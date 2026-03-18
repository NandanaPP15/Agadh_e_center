import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.utils import timezone
from .models import ChatMessage, UserSession
from .llm.query_processor import QueryProcessor
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'chat_{self.session_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Update session activity
        await self.update_session_activity()
        
        logger.info(f"WebSocket connected for session: {self.session_id}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        logger.info(f"WebSocket disconnected for session: {self.session_id}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'chat_message')
            
            if message_type == 'chat_message':
                message = text_data_json['message']
                user_id = text_data_json.get('user_id')
                language = text_data_json.get('language', 'en')
                
                # Save user message
                await self.save_message(
                    message_type='user',
                    content=message,
                    language=language,
                    user_id=user_id
                )
                
                # Process message with NLP
                processor = QueryProcessor()
                response_data = processor.process_query(message, self.session_id)
                
                # Send bot response
                await self.send_bot_response(response_data)
                
                # Broadcast to group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender': 'user',
                        'timestamp': timezone.now().isoformat(),
                        'user_id': user_id
                    }
                )
            
            elif message_type == 'typing_indicator':
                # Broadcast typing indicator
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_indicator',
                        'user_id': text_data_json.get('user_id'),
                        'is_typing': text_data_json.get('is_typing', False)
                    }
                )
            
            elif message_type == 'employee_joined':
                # Notify that employee joined chat
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'employee_joined',
                        'employee_id': text_data_json.get('employee_id'),
                        'employee_name': text_data_json.get('employee_name')
                    }
                )
            
            elif message_type == 'file_uploaded':
                # Handle file upload notification
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'file_uploaded',
                        'file_name': text_data_json.get('file_name'),
                        'file_url': text_data_json.get('file_url'),
                        'user_id': text_data_json.get('user_id')
                    }
                )
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error in receive: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Internal server error'
            }))

    async def send_bot_response(self, response_data):
        """Send bot response to client"""
        bot_response = {
            'type': 'bot_message',
            'message': response_data['response'],
            'intent': response_data.get('intent'),
            'service': response_data.get('service'),
            'needs_login': response_data.get('needs_login', False),
            'employee_connect': response_data.get('employee_connect', False),
            'timestamp': timezone.now().isoformat()
        }
        
        # Send to client
        await self.send(text_data=json.dumps(bot_response))
        
        # Save bot message
        await self.save_message(
            message_type='bot',
            content=response_data['response'],
            language=response_data.get('language', 'en'),
            metadata={
                'intent': response_data.get('intent'),
                'service': response_data.get('service')
            }
        )

    async def chat_message(self, event):
        """Receive chat message from room group"""
        await self.send(text_data=json.dumps({
            'type': 'user_message',
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
            'user_id': event.get('user_id')
        }))

    async def typing_indicator(self, event):
        """Receive typing indicator from room group"""
        await self.send(text_data=json.dumps({
            'type': 'typing_indicator',
            'user_id': event['user_id'],
            'is_typing': event['is_typing']
        }))

    async def employee_joined(self, event):
        """Receive employee joined notification"""
        await self.send(text_data=json.dumps({
            'type': 'employee_joined',
            'employee_id': event['employee_id'],
            'employee_name': event['employee_name'],
            'timestamp': timezone.now().isoformat()
        }))

    async def file_uploaded(self, event):
        """Receive file uploaded notification"""
        await self.send(text_data=json.dumps({
            'type': 'file_uploaded',
            'file_name': event['file_name'],
            'file_url': event['file_url'],
            'user_id': event['user_id'],
            'timestamp': timezone.now().isoformat()
        }))

    @database_sync_to_async
    def save_message(self, message_type, content, language='en', user_id=None, metadata=None):
        """Save chat message to database"""
        try:
            session = UserSession.objects.get(session_id=self.session_id)
            
            # If user_id provided, update session user
            if user_id and not session.user:
                from users.models import User
                try:
                    user = User.objects.get(id=user_id)
                    session.user = user
                    session.save()
                except User.DoesNotExist:
                    pass
            
            message = ChatMessage.objects.create(
                session=session,
                message_type=message_type,
                content=content,
                language=language,
                metadata=metadata or {}
            )
            
            return message.id
        except UserSession.DoesNotExist:
            logger.error(f"Session not found: {self.session_id}")
            return None
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return None

    @database_sync_to_async
    def update_session_activity(self):
        """Update session last activity timestamp"""
        try:
            session = UserSession.objects.get(session_id=self.session_id)
            session.last_activity = timezone.now()
            session.save()
        except UserSession.DoesNotExist:
            logger.error(f"Session not found for activity update: {self.session_id}")


class EmployeeChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for employee-citizen chat sessions"""
    
    async def connect(self):
        self.employee_id = self.scope['url_route']['kwargs']['employee_id']
        self.chat_session_id = self.scope['url_route']['kwargs']['chat_session_id']
        self.room_group_name = f'employee_chat_{self.chat_session_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Notify that employee joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'employee_connected',
                'employee_id': self.employee_id,
                'timestamp': timezone.now().isoformat()
            }
        )
        
        logger.info(f"Employee WebSocket connected: {self.employee_id}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        logger.info(f"Employee WebSocket disconnected: {self.employee_id}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'chat_message')
            
            if message_type == 'chat_message':
                message = data['message']
                sender_type = data.get('sender_type', 'employee')
                
                # Save message
                await self.save_employee_chat_message(
                    message=message,
                    sender_type=sender_type,
                    employee_id=self.employee_id
                )
                
                # Broadcast to room
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'employee_chat_message',
                        'message': message,
                        'sender_type': sender_type,
                        'employee_id': self.employee_id,
                        'timestamp': timezone.now().isoformat()
                    }
                )
            
            elif message_type == 'document_request':
                # Handle document request from employee
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'document_request',
                        'document_types': data.get('document_types', []),
                        'employee_id': self.employee_id,
                        'instructions': data.get('instructions', '')
                    }
                )
            
            elif message_type == 'service_update':
                # Handle service status update
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'service_update',
                        'status': data.get('status'),
                        'employee_id': self.employee_id,
                        'notes': data.get('notes', '')
                    }
                )
        
        except Exception as e:
            logger.error(f"Error in employee receive: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Internal server error'
            }))

    async def employee_chat_message(self, event):
        """Receive chat message in employee chat"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender_type': event['sender_type'],
            'employee_id': event['employee_id'],
            'timestamp': event['timestamp']
        }))

    async def employee_connected(self, event):
        """Notify that employee connected"""
        await self.send(text_data=json.dumps({
            'type': 'employee_connected',
            'employee_id': event['employee_id'],
            'timestamp': event['timestamp']
        }))

    async def document_request(self, event):
        """Receive document request"""
        await self.send(text_data=json.dumps({
            'type': 'document_request',
            'document_types': event['document_types'],
            'employee_id': event['employee_id'],
            'instructions': event['instructions'],
            'timestamp': timezone.now().isoformat()
        }))

    async def service_update(self, event):
        """Receive service update"""
        await self.send(text_data=json.dumps({
            'type': 'service_update',
            'status': event['status'],
            'employee_id': event['employee_id'],
            'notes': event['notes'],
            'timestamp': timezone.now().isoformat()
        }))

    @database_sync_to_async
    def save_employee_chat_message(self, message, sender_type, employee_id):
        """Save employee chat message"""
        try:
            from employees.models import EmployeeChatSession
            chat_session = EmployeeChatSession.objects.get(
                session_id=self.chat_session_id,
                employee__employee_id=employee_id
            )
            
            # Save message to database
            ChatMessage.objects.create(
                session=chat_session.session,  # Link to user session
                message_type=sender_type,
                content=message,
                metadata={'chat_session_id': self.chat_session_id}
            )
            
            # Update chat session metrics
            chat_session.increment_message_count(sender_type)
            
        except Exception as e:
            logger.error(f"Error saving employee chat message: {e}")