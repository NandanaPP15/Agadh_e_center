"""
Custom actions for Agadh chatbot
"""
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionGreet(Action):
    """Simple greet action"""
    
    def name(self) -> Text:
        return "action_greet"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_greet")
        return []

class ActionGetServiceDocuments(Action):
    """Get document requirements for a specific service"""
    
    def name(self) -> Text:
        return "action_get_service_documents"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get user message
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Check for service keywords
        if 'ration' in user_message:
            dispatcher.utter_message(response="utter_ration_card_docs")
        elif 'passport' in user_message:
            dispatcher.utter_message(response="utter_passport_docs")
        elif 'aadhaar' in user_message or 'aadhar' in user_message:
            dispatcher.utter_message(response="utter_aadhaar_docs")
        elif 'pan' in user_message:
            dispatcher.utter_message(text="For PAN Card, you need:\n1. Identity Proof (Aadhaar/Passport)\n2. Address Proof\n3. Date of Birth Proof\n4. Passport-size photos\n\nProcessing: 15-20 days\nFee: ₹107")
        elif 'marriage' in user_message:
            dispatcher.utter_message(text="For Marriage Registration, you need:\n1. Age Proof\n2. Address Proof\n3. Marriage Proof\n4. Photos\n5. Witness Details\n\nProcessing: 3-5 days\nFee: ₹100")
        elif 'police' in user_message or 'pcc' in user_message:
            dispatcher.utter_message(text="For Police Clearance Certificate, you need:\n1. Passport copy\n2. Address Proof\n3. Identity Proof\n4. Photos\n5. Application form\n\nProcessing: 10-15 days\nFee: ₹500")
        elif 'birth' in user_message:
            dispatcher.utter_message(text="For Birth Certificate, you need:\n1. Hospital birth report\n2. Parent's ID proof\n3. Parent's address proof\n4. Marriage certificate\n\nProcessing: 3-7 days\nFee: ₹30")
        elif 'death' in user_message:
            dispatcher.utter_message(text="For Death Registration, you need:\n1. Medical certificate\n2. Deceased ID proof\n3. Informant ID proof\n4. Address proof\n\nProcessing: 3-7 days\nFee: ₹30")
        elif 'ncl' in user_message or 'non creamy' in user_message:
            dispatcher.utter_message(text="For NCL Certificate, you need:\n1. Community certificate\n2. Income certificate\n3. Ration card\n4. Aadhaar card\n5. Educational certificates\n\nProcessing: 10-15 days\nFee: ₹100")
        else:
            dispatcher.utter_message(response="utter_ask_services")
        
        return []

class ActionFallback(Action):
    """Fallback action"""
    
    def name(self) -> Text:
        return "action_fallback"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_fallback")
        return []