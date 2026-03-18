"""
Intent classification for user queries
"""
import re
from typing import Dict, List, Any
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

from .language_detector import LanguageDetector

class IntentClassifier:
    """
    Classifies user intent for government service queries
    """
    
    # Intent categories
    INTENTS = {
        'service_inquiry': 'Service Information',
        'document_requirements': 'Document Requirements',
        'application_process': 'Application Process',
        'fee_inquiry': 'Fee Information',
        'status_check': 'Application Status',
        'location_finder': 'Service Center Location',
        'employee_contact': 'Employee Contact',
        'greeting': 'Greeting',
        'farewell': 'Farewell',
        'thanks': 'Thanks',
        'help': 'Help Request',
        'unknown': 'Unknown'
    }
    
    # Service mapping keywords
    SERVICE_KEYWORDS = {
        'ration_card': [
            'ration', 'ration card', 'food card', 'rationcard',
            'റേഷൻ', 'റേഷൻ കാർഡ്', 'ഭക്ഷണ കാർഡ്'
        ],
        'marriage_registration': [
            'marriage', 'wedding', 'marriage registration', 'marriage certificate',
            'വിവാഹം', 'വിവാഹ രജിസ്ട്രേഷൻ', 'വിവാഹ സർട്ടിഫിക്കറ്റ്'
        ],
        'police_clearance': [
            'pcc', 'police clearance', 'police certificate', 'character certificate',
            'പോലീസ്', 'പോലീസ് ക്ലിയറൻസ്', 'പോലീസ് സർട്ടിഫിക്കറ്റ്'
        ],
        'pan_card': [
            'pan', 'pan card', 'permanent account number',
            'പാൻ', 'പാൻ കാർഡ്', 'പെർമനന്റ് അക്കൗണ്ട് നമ്പർ'
        ],
        'birth_certificate': [
            'birth', 'birth certificate', 'date of birth', 'dob certificate',
            'ജനനം', 'ജനന സർട്ടിഫിക്കറ്റ്', 'ജനന തീയതി'
        ],
        'passport': [
            'passport', 'passport service', 'passport renewal',
            'പാസ്പോർട്ട്', 'പാസ്പോർട്ട് സേവനം', 'പാസ്പോർട്ട് പുതുക്കൽ'
        ],
        'aadhaar': [
            'aadhaar', 'aadhar', 'uid', 'unique id',
            'ആധാർ', 'യൂണിക് ഐഡി', 'യുണിക്യൂ ഐഡന്റിറ്റി'
        ],
        'death_registration': [
            'death', 'death certificate', 'demise certificate',
            'മരണം', 'മരണ സർട്ടിഫിക്കറ്റ്', 'മരണ രജിസ്ട്രേഷൻ'
        ],
        'ncl_certificate': [
            'ncl', 'non creamy layer', 'caste certificate', 'community certificate',
            'എൻസിഎൽ', 'നോൺ ക്രീം ലെയർ', 'ജാതി സർട്ടിഫിക്കറ്റ്'
        ]
    }
    
    # Document keywords
    DOCUMENT_KEYWORDS = [
        'document', 'documents', 'required', 'need', 'require',
        'paper', 'papers', 'proof', 'evidence', 'certificate',
        'ദസ്താവേജ്', 'ദസ്താവേജുകൾ', 'ആവശ്യമായ', 'തെളിവ്', 'സർട്ടിഫിക്കറ്റ്'
    ]
    
    def __init__(self):
        """Initialize intent classifier"""
        self.language_detector = LanguageDetector()
        self.vectorizer = None
        self.classifier = None
        self.stop_words = set(stopwords.words('english'))
        
        # Add Malayalam stopwords
        self.malayalam_stopwords = set([
            'ഒരു', 'അത്', 'ഇത്', 'ആണ്', 'ഉണ്ട്', 'എന്ത്', 'എങ്ങനെ',
            'എവിടെ', 'എപ്പോൾ', 'ആര്', 'ഇല്ല', 'പോലെ', 'കൂടെ'
        ])
        
        # Try to load pre-trained model
        self.model_path = os.path.join(os.path.dirname(__file__), 'intent_model.pkl')
        self._load_or_train_model()
    
    def _load_or_train_model(self):
        """Load pre-trained model or train new one"""
        try:
            if os.path.exists(self.model_path):
                model_data = joblib.load(self.model_path)
                self.vectorizer = model_data['vectorizer']
                self.classifier = model_data['classifier']
            else:
                self._train_model()
        except:
            self._train_model()
    
    def _train_model(self):
        """Train intent classification model"""
        # Training data
        training_data = [
            # Service inquiries
            ("What services do you provide?", 'service_inquiry'),
            ("Tell me about government services", 'service_inquiry'),
            ("What are the available services?", 'service_inquiry'),
            ("സേവനങ്ങൾ എന്തെല്ലാം ഉണ്ട്?", 'service_inquiry'),
            
            # Document requirements
            ("What documents are required for ration card?", 'document_requirements'),
            ("What do I need for passport application?", 'document_requirements'),
            ("Required documents for marriage registration", 'document_requirements'),
            ("റേഷൻ കാർഡിന് എന്ത് ഡോക്കുമെന്റ് വേണം?", 'document_requirements'),
            
            # Application process
            ("How to apply for pan card?", 'application_process'),
            ("What is the process for birth certificate?", 'application_process'),
            ("Steps to get police clearance", 'application_process'),
            ("പാൻ കാർഡിന് എങ്ങനെ അപേക്ഷിക്കാം?", 'application_process'),
            
            # Fee inquiries
            ("How much for ration card?", 'fee_inquiry'),
            ("What is the fee for passport?", 'fee_inquiry'),
            ("Cost of marriage registration", 'fee_inquiry'),
            ("റേഷൻ കാർഡിന് എത്ര ഫീസ്?", 'fee_inquiry'),
            
            # Greetings
            ("Hello", 'greeting'),
            ("Hi", 'greeting'),
            ("Good morning", 'greeting'),
            ("നമസ്കാരം", 'greeting'),
            
            # Thanks
            ("Thank you", 'thanks'),
            ("Thanks", 'thanks'),
            ("നന്ദി", 'thanks'),
            
            # Help
            ("Help", 'help'),
            ("Can you help me?", 'help'),
            ("സഹായിക്കാമോ?", 'help'),
        ]
        
        # Prepare training data
        texts = [data[0] for data in training_data]
        intents = [data[1] for data in training_data]
        
        # Vectorize text
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        X = self.vectorizer.fit_transform(texts)
        
        # Train classifier
        self.classifier = MultinomialNB()
        self.classifier.fit(X, intents)
        
        # Save model
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier
        }
        joblib.dump(model_data, self.model_path)
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for classification
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def classify(self, query: str, language: str = 'en') -> Dict[str, Any]:
        """
        Classify user query intent
        
        Args:
            query: User query
            language: Query language
            
        Returns:
            Dictionary with classification results
        """
        if not query:
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'service_type': None,
                'response': "Please provide a query.",
                'suggestions': []
            }
        
        # Detect language if not specified
        if language == 'auto':
            detection = self.language_detector.detect(query)
            language = detection['language']
            if detection['language'] == 'ml':
                query = self.language_detector.translate_to_english(query)
        
        # Preprocess query
        processed_query = self.preprocess_text(query)
        
        # Extract service type
        service_type = self._extract_service_type(query, language)
        
        # Extract intent using ML model
        ml_intent, ml_confidence = self._classify_with_ml(processed_query)
        
        # Rule-based intent detection
        rule_intent, rule_confidence = self._classify_with_rules(query, language, service_type)
        
        # Combine results (prefer rule-based for document queries)
        if rule_confidence > ml_confidence:
            intent = rule_intent
            confidence = rule_confidence
        else:
            intent = ml_intent
            confidence = ml_confidence
        
        # Generate response
        response = self._generate_response(intent, service_type, language)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(intent, service_type, language)
        
        return {
            'intent': intent,
            'intent_display': self.INTENTS.get(intent, 'Unknown'),
            'confidence': confidence,
            'service_type': service_type,
            'language': language,
            'response': response,
            'suggestions': suggestions,
            'processed_query': processed_query
        }
    
    def _extract_service_type(self, query: str, language: str) -> str:
        """
        Extract service type from query
        
        Args:
            query: User query
            language: Query language
            
        Returns:
            Service type identifier or None
        """
        query_lower = query.lower()
        
        for service_type, keywords in self.SERVICE_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    return service_type
        
        return None
    
    def _classify_with_ml(self, query: str) -> tuple:
        """
        Classify intent using ML model
        
        Args:
            query: Preprocessed query
            
        Returns:
            Tuple of (intent, confidence)
        """
        try:
            X = self.vectorizer.transform([query])
            probabilities = self.classifier.predict_proba(X)[0]
            intent_idx = probabilities.argmax()
            confidence = probabilities[intent_idx]
            intent = self.classifier.classes_[intent_idx]
            return intent, confidence
        except:
            return 'unknown', 0.0
    
    def _classify_with_rules(self, query: str, language: str, service_type: str) -> tuple:
        """
        Classify intent using rule-based approach
        
        Args:
            query: User query
            language: Query language
            service_type: Extracted service type
            
        Returns:
            Tuple of (intent, confidence)
        """
        query_lower = query.lower()
        
        # Document requirements
        doc_keywords = self.DOCUMENT_KEYWORDS
        if any(keyword in query_lower for keyword in doc_keywords) and service_type:
            return 'document_requirements', 0.95
        
        # Application process
        process_keywords = ['how to', 'process', 'steps', 'procedure', 'apply', 
                           'എങ്ങനെ', 'പ്രക്രിയ', 'ഘട്ടങ്ങൾ']
        if any(keyword in query_lower for keyword in process_keywords) and service_type:
            return 'application_process', 0.90
        
        # Fee inquiry
        fee_keywords = ['fee', 'cost', 'price', 'charge', 'how much', 
                       'ഫീസ്', 'വില', 'എത്ര']
        if any(keyword in query_lower for keyword in fee_keywords) and service_type:
            return 'fee_inquiry', 0.85
        
        # Service inquiry
        if service_type:
            return 'service_inquiry', 0.80
        
        # Greetings
        greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon',
                            'good evening', 'നമസ്കാരം', 'ഹലോ']
        if any(keyword in query_lower for keyword in greeting_keywords):
            return 'greeting', 0.95
        
        # Thanks
        thanks_keywords = ['thank', 'thanks', 'നന്ദി', 'ധന്യവാദം']
        if any(keyword in query_lower for keyword in thanks_keywords):
            return 'thanks', 0.90
        
        # Help
        help_keywords = ['help', 'സഹായം', 'സഹായിക്ക']
        if any(keyword in query_lower for keyword in help_keywords):
            return 'help', 0.85
        
        return 'unknown', 0.5
    
    def _generate_response(self, intent: str, service_type: str, language: str) -> str:
        """
        Generate response based on intent
        
        Args:
            intent: Detected intent
            service_type: Service type
            language: Response language
            
        Returns:
            Response text
        """
        service_name = None
        if service_type:
            service_name = self.language_detector.get_service_in_language(service_type, language)
        
        responses = {
            'service_inquiry': {
                'en': f"I can help you with {service_name if service_name else 'government services'}. What specific information do you need?",
                'ml': f"എനിക്ക് {service_name if service_name else 'സർക്കാർ സേവനങ്ങളിൽ'} സഹായിക്കാൻ കഴിയും. നിങ്ങൾക്ക് എന്ത് വിവരം വേണം?"
            },
            'document_requirements': {
                'en': f"For {service_name if service_name else 'this service'}, you'll need several documents. Let me list them for you.",
                'ml': f"{service_name if service_name else 'ഈ സേവനത്തിന്'} നിരവധി ഡോക്കുമെന്റുകൾ വേണം. ഞാൻ അവ ലിസ്റ്റ് ചെയ്യാം."
            },
            'application_process': {
                'en': f"The application process for {service_name if service_name else 'this service'} involves several steps. Here's how to apply:",
                'ml': f"{service_name if service_name else 'ഈ സേവനത്തിനുള്ള'} അപേക്ഷാ പ്രക്രിയയിൽ നിരവധി ഘട്ടങ്ങൾ ഉൾപ്പെടുന്നു. ഇങ്ങനെയാണ് അപേക്ഷിക്കേണ്ടത്:"
            },
            'fee_inquiry': {
                'en': f"The fee for {service_name if service_name else 'this service'} varies. Let me check the exact amount for you.",
                'ml': f"{service_name if service_name else 'ഈ സേവനത്തിനുള്ള'} ഫീസ് വ്യത്യാസപ്പെട്ടിരിക്കുന്നു. കൃത്യമായ തുക ഞാൻ പരിശോധിക്കാം."
            },
            'greeting': {
                'en': "Hello! Welcome to Agadh e-Center Digitization. How can I assist you with government services today?",
                'ml': "നമസ്കാരം! അഗാധ് ഇ-സെന്റർ ഡിജിറ്റലൈസേഷനിലേക്ക് സ്വാഗതം. ഇന്ന് സർക്കാർ സേവനങ്ങളിൽ എങ്ങനെ സഹായിക്കാം?"
            },
            'thanks': {
                'en': "You're welcome! Is there anything else I can help you with?",
                'ml': "നിങ്ങൾക്ക് സ്വാഗതം! എനിക്ക് മറ്റെന്തെങ്കിലും സഹായിക്കാനുണ്ടോ?"
            },
            'help': {
                'en': "I'm here to help! You can ask me about government services, document requirements, application processes, fees, and more.",
                'ml': "ഞാൻ സഹായിക്കാൻ ഇവിടെയുണ്ട്! സർക്കാർ സേവനങ്ങൾ, ഡോക്കുമെന്റ് ആവശ്യങ്ങൾ, അപേക്ഷാ പ്രക്രിയ, ഫീസ് എന്നിവയെക്കുറിച്ച് നിങ്ങൾക്ക് എന്നോട് ചോദിക്കാം."
            },
            'unknown': {
                'en': "I'm not sure I understand. Could you please rephrase your question? You can ask about government services, documents, or application processes.",
                'ml': "എനിക്ക് മനസ്സിലായില്ല. ദയവായി നിങ്ങളുടെ ചോദ്യം വീണ്ടും ചോദിക്കാമോ? സർക്കാർ സേവനങ്ങൾ, ഡോക്കുമെന്റുകൾ അല്ലെങ്കിൽ അപേക്ഷാ പ്രക്രിയയെക്കുറിച്ച് നിങ്ങൾക്ക് ചോദിക്കാം."
            }
        }
        
        intent_responses = responses.get(intent, responses['unknown'])
        return intent_responses.get(language, intent_responses['en'])
    
    def _generate_suggestions(self, intent: str, service_type: str, language: str) -> List[str]:
        """
        Generate follow-up suggestions
        
        Args:
            intent: Detected intent
            service_type: Service type
            language: Language for suggestions
            
        Returns:
            List of suggestion strings
        """
        suggestions = []
        
        if intent == 'service_inquiry' and service_type:
            if language == 'ml':
                suggestions = [
                    f"{service_type.replace('_', ' ').title()} സേവനങ്ങളെക്കുറിച്ച് കൂടുതൽ വിവരങ്ങൾ",
                    f"{service_type.replace('_', ' ').title()} ഡോക്കുമെന്റ് ആവശ്യങ്ങൾ",
                    f"{service_type.replace('_', ' ').title()} അപേക്ഷാ പ്രക്രിയ",
                    f"{service_type.replace('_', ' ').title()} ഫീസ് വിവരങ്ങൾ"
                ]
            else:
                suggestions = [
                    f"More details about {service_type.replace('_', ' ')} services",
                    f"Document requirements for {service_type.replace('_', ' ')}",
                    f"Application process for {service_type.replace('_', ' ')}",
                    f"Fee information for {service_type.replace('_', ' ')}"
                ]
        elif intent == 'greeting':
            if language == 'ml':
                suggestions = [
                    "റേഷൻ കാർഡ് സേവനങ്ങൾ",
                    "പാസ്പോർട്ട് സേവനങ്ങൾ",
                    "ആധാർ സേവനങ്ങൾ",
                    "വിവാഹ രജിസ്ട്രേഷൻ"
                ]
            else:
                suggestions = [
                    "Ration Card Services",
                    "Passport Services",
                    "Aadhaar Services",
                    "Marriage Registration"
                ]
        
        return suggestions