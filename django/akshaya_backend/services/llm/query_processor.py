"""
Query processing module for NLP tasks
"""
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

from .language_detector import LanguageDetector
from .intent_classifier import IntentClassifier
from ..models import Service, DocumentType

class QueryProcessor:
    """
    Processes user queries and extracts relevant information
    """
    
    def __init__(self):
        """Initialize query processor"""
        self.language_detector = LanguageDetector()
        self.intent_classifier = IntentClassifier()
        
        # Document patterns
        self.document_patterns = {
            'aadhaar': [r'aadhaar', r'aadhar', r'uid', r'ആധാർ'],
            'pan': [r'pan', r'pan card', r'പാൻ'],
            'voter_id': [r'voter', r'voter id', r'വോട്ടർ'],
            'passport': [r'passport', r'പാസ്പോർട്ട്'],
            'driving_license': [r'driving', r'dl', r'license', r'ഡ്രൈവിംഗ്'],
            'birth_certificate': [r'birth', r'birth certificate', r'ജനന'],
            'death_certificate': [r'death', r'death certificate', r'മരണ'],
            'income_certificate': [r'income', r'income certificate', r'ഇൻകം'],
            'address_proof': [r'address', r'address proof', r'വിലാസം'],
            'identity_proof': [r'identity', r'id proof', r'ഐഡന്റിറ്റി']
        }
    
    def process(self, query: str, user_language: str = 'auto') -> Dict[str, Any]:
        """
        Process user query
        
        Args:
            query: User query
            user_language: Preferred language
            
        Returns:
            Dictionary with processed results
        """
        # Language detection
        lang_detection = self.language_detector.detect(query)
        
        # Use detected language if auto, otherwise use specified
        if user_language == 'auto':
            language = lang_detection['language']
        else:
            language = user_language
        
        # Translate to English for processing if needed
        if language == 'ml':
            english_query = self.language_detector.translate_to_english(query)
        else:
            english_query = query
        
        # Intent classification
        classification = self.intent_classifier.classify(english_query, language)
        
        # Extract entities
        entities = self._extract_entities(english_query, language)
        
        # Get service information if service type is detected
        service_info = None
        if classification['service_type']:
            service_info = self._get_service_info(
                classification['service_type'],
                language
            )
        
        # Get document requirements if relevant
        documents = None
        if (classification['intent'] == 'document_requirements' and 
            classification['service_type']):
            documents = self._get_document_requirements(
                classification['service_type'],
                language
            )
        
        # Generate detailed response
        detailed_response = self._generate_detailed_response(
            classification,
            service_info,
            documents,
            language
        )
        
        return {
            'query': query,
            'original_language': lang_detection['language'],
            'processed_language': language,
            'classification': classification,
            'entities': entities,
            'service_info': service_info,
            'documents': documents,
            'response': detailed_response,
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_entities(self, query: str, language: str) -> Dict[str, List]:
        """
        Extract entities from query
        
        Args:
            query: User query
            language: Query language
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {
            'documents': [],
            'services': [],
            'locations': [],
            'dates': [],
            'numbers': []
        }
        
        # Extract document mentions
        for doc_type, patterns in self.document_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    entities['documents'].append(doc_type)
                    break
        
        # Extract service mentions
        for service_type, keywords in self.intent_classifier.SERVICE_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in query.lower():
                    entities['services'].append(service_type)
                    break
        
        # Extract numbers (fees, etc.)
        numbers = re.findall(r'\b\d+\b', query)
        if numbers:
            entities['numbers'] = [int(n) for n in numbers]
        
        return entities
    
    def _get_service_info(self, service_type: str, language: str) -> Optional[Dict]:
        """
        Get service information from database
        
        Args:
            service_type: Service type identifier
            language: Language for response
            
        Returns:
            Service information dictionary or None
        """
        try:
            service = Service.objects.get(service_type=service_type, is_active=True)
            
            # Get service name in target language
            service_name = self.language_detector.get_service_in_language(
                service_type, language
            )
            
            return {
                'id': service.id,
                'name': service_name,
                'description': service.description,
                'processing_time': service.processing_time,
                'fee': float(service.fee),
                'online_available': service.online_available,
                'department': service.department,
                'slug': service.slug
            }
        except Service.DoesNotExist:
            return None
    
    def _get_document_requirements(self, service_type: str, language: str) -> Optional[List[Dict]]:
        """
        Get document requirements for a service
        
        Args:
            service_type: Service type identifier
            language: Language for response
            
        Returns:
            List of document requirements or None
        """
        try:
            service = Service.objects.get(service_type=service_type, is_active=True)
            documents = service.required_documents.filter(is_active=True)
            
            document_list = []
            for doc in documents:
                document_list.append({
                    'name': doc.name,
                    'description': doc.description,
                    'is_mandatory': doc.is_mandatory,
                    'max_size_mb': doc.max_size_mb,
                    'example_url': doc.example_url
                })
            
            return document_list
        except Service.DoesNotExist:
            return None
    
    def _generate_detailed_response(self, classification: Dict, 
                                   service_info: Optional[Dict],
                                   documents: Optional[List],
                                   language: str) -> Dict[str, Any]:
        """
        Generate detailed response based on classification
        
        Args:
            classification: Intent classification results
            service_info: Service information
            documents: Document requirements
            language: Response language
            
        Returns:
            Detailed response dictionary
        """
        intent = classification['intent']
        service_type = classification['service_type']
        
        response = {
            'summary': classification['response'],
            'details': {},
            'action_items': [],
            'next_steps': []
        }
        
        if intent == 'document_requirements' and documents:
            if language == 'ml':
                response['details']['documents'] = {
                    'title': 'ആവശ്യമായ ഡോക്കുമെന്റുകൾ',
                    'items': documents
                }
                response['action_items'].append('ഡോക്കുമെന്റുകൾ തയ്യാറാക്കുക')
                response['action_items'].append('ഓൺലൈനിൽ അപ്ലൈ ചെയ്യുക')
                response['next_steps'].append('അടുത്തതായി അപേക്ഷാ പ്രക്രിയ ചോദിക്കുക')
            else:
                response['details']['documents'] = {
                    'title': 'Required Documents',
                    'items': documents
                }
                response['action_items'].append('Prepare the documents')
                response['action_items'].append('Apply online')
                response['next_steps'].append('Ask about application process next')
        
        elif intent == 'service_inquiry' and service_info:
            if language == 'ml':
                response['details']['service'] = {
                    'title': 'സേവന വിവരങ്ങൾ',
                    'items': [
                        {'label': 'വിഭാഗം', 'value': service_info['department']},
                        {'label': 'പ്രോസസ്സിംഗ് സമയം', 'value': service_info['processing_time']},
                        {'label': 'ഫീസ്', 'value': f"₹{service_info['fee']}"},
                        {'label': 'ഓൺലൈൻ ലഭ്യത', 'value': 'ഉണ്ട്' if service_info['online_available'] else 'ഇല്ല'}
                    ]
                }
                response['next_steps'].append('ഡോക്കുമെന്റ് ആവശ്യങ്ങൾ ചോദിക്കുക')
                response['next_steps'].append('അപേക്ഷാ പ്രക്രിയ ചോദിക്കുക')
            else:
                response['details']['service'] = {
                    'title': 'Service Information',
                    'items': [
                        {'label': 'Department', 'value': service_info['department']},
                        {'label': 'Processing Time', 'value': service_info['processing_time']},
                        {'label': 'Fee', 'value': f"₹{service_info['fee']}"},
                        {'label': 'Online Available', 'value': 'Yes' if service_info['online_available'] else 'No'}
                    ]
                }
                response['next_steps'].append('Ask about document requirements')
                response['next_steps'].append('Ask about application process')
        
        elif intent == 'application_process' and service_info:
            if language == 'ml':
                response['details']['process'] = {
                    'title': 'അപേക്ഷാ പ്രക്രിയ',
                    'steps': [
                        'ഡോക്കുമെന്റുകൾ തയ്യാറാക്കുക',
                        'ഓൺലൈൻ ഫോം പൂരിപ്പിക്കുക',
                        'ഡോക്കുമെന്റുകൾ അപ്ലോഡ് ചെയ്യുക',
                        'ഫീസ് അടയ്ക്കുക',
                        'അപേക്ഷ സമർപ്പിക്കുക'
                    ]
                }
            else:
                response['details']['process'] = {
                    'title': 'Application Process',
                    'steps': [
                        'Prepare required documents',
                        'Fill online application form',
                        'Upload documents',
                        'Pay the fee',
                        'Submit application'
                    ]
                }
        
        return response
    
    def batch_process(self, queries: List[str], language: str = 'en') -> List[Dict]:
        """
        Process multiple queries
        
        Args:
            queries: List of user queries
            language: Language for processing
            
        Returns:
            List of processed results
        """
        results = []
        for query in queries:
            try:
                result = self.process(query, language)
                results.append(result)
            except Exception as e:
                results.append({
                    'query': query,
                    'error': str(e),
                    'response': "Sorry, I couldn't process this query."
                })
        
        return results
    
    def get_related_queries(self, processed_result: Dict) -> List[str]:
        """
        Get related queries based on processed result
        
        Args:
            processed_result: Processed query result
            
        Returns:
            List of related queries
        """
        classification = processed_result['classification']
        language = processed_result['processed_language']
        service_type = classification['service_type']
        
        if not service_type:
            return []
        
        service_name = self.language_detector.get_service_in_language(
            service_type, language
        )
        
        if language == 'ml':
            return [
                f"{service_name} ഡോക്കുമെന്റ് ആവശ്യങ്ങൾ എന്താണ്?",
                f"{service_name} അപേക്ഷിക്കുന്നത് എങ്ങനെ?",
                f"{service_name} ഫീസ് എത്രയാണ്?",
                f"{service_name} പ്രോസസ്സിംഗ് സമയം എത്ര ദിവസമാണ്?"
            ]
        else:
            return [
                f"What documents are required for {service_name}?",
                f"How to apply for {service_name}?",
                f"What is the fee for {service_name}?",
                f"What is the processing time for {service_name}?"
            ]