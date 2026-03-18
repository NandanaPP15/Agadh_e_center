"""
Language detection module for English and Malayalam
"""
import re
from typing import Dict, Tuple
import nltk
from googletrans import Translator

class LanguageDetector:
    """Detects language of input text (English/Malayalam/Manglish)"""
    
    # Common Malayalam words and patterns
    MALAYALAM_KEYWORDS = [
        'ഹലോ', 'നമസ്കാരം', 'സേവനങ്ങൾ', 'വിവരങ്ങൾ', 'ദസ്താവേജ്',
        'അപേക്ഷ', 'സർട്ടിഫിക്കറ്റ്', 'കാർഡ്', 'രജിസ്ട്രേഷൻ',
        'ജനനം', 'മരണം', 'വിവാഹം', 'പാസ്പോർട്ട്', 'പാൻ',
        'ആധാർ', 'റേഷൻ', 'പോലീസ്', 'സർട്ടിഫിക്കറ്റ്'
    ]
    
    # Service keywords in Malayalam
    MALAYALAM_SERVICES = {
        'ration_card': 'റേഷൻ കാർഡ്',
        'marriage_registration': 'വിവാഹ രജിസ്ട്രേഷൻ',
        'police_clearance': 'പോലീസ് ക്ലിയറൻസ് സർട്ടിഫിക്കറ്റ്',
        'pan_card': 'പാൻ കാർഡ്',
        'birth_certificate': 'ജനന സർട്ടിഫിക്കറ്റ്',
        'passport': 'പാസ്പോർട്ട്',
        'aadhaar': 'ആധാർ',
        'death_registration': 'മരണ രജിസ്ട്രേഷൻ',
        'ncl_certificate': 'നോൺ ക്രീം ലെയർ സർട്ടിഫിക്കറ്റ്'
    }
    
    def __init__(self):
        """Initialize language detector"""
        self.translator = Translator()
        
    def detect(self, text: str) -> Dict:
        """
        Detect language of input text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with language detection results
        """
        if not text or not isinstance(text, str):
            return {'language': 'en', 'confidence': 0.0, 'original': text}
        
        text = text.strip()
        
        # Check for Malayalam script (Unicode range: 0D00-0D7F)
        malayalam_chars = re.findall(r'[\u0D00-\u0D7F]', text)
        malayalam_ratio = len(malayalam_chars) / len(text) if text else 0
        
        # Check for English (Latin script)
        english_chars = re.findall(r'[a-zA-Z]', text)
        english_ratio = len(english_chars) / len(text) if text else 0
        
        # Check for common Malayalam keywords (transliterated)
        malayalam_keyword_count = 0
        for keyword in self.MALAYALAM_KEYWORDS:
            if keyword.lower() in text.lower():
                malayalam_keyword_count += 1
        
        # Determine language
        if malayalam_ratio > 0.3 or malayalam_keyword_count > 2:
            language = 'ml'
            confidence = min(0.9, (malayalam_ratio * 2 + malayalam_keyword_count / 5))
        elif english_ratio > 0.7:
            language = 'en'
            confidence = english_ratio
        else:
            # Check for Manglish (mix of English and transliterated Malayalam)
            if any(keyword in text.lower() for keyword in [
                'ration', 'pan', 'aadhaar', 'passport', 
                'birth', 'death', 'marriage', 'police'
            ]):
                language = 'en'  # Treat as English for simplicity
                confidence = 0.8
            else:
                language = 'en'
                confidence = 0.5
        
        return {
            'language': language,
            'confidence': round(confidence, 2),
            'original': text,
            'is_malayalam': language == 'ml',
            'is_english': language == 'en'
        }
    
    def translate_to_english(self, text: str) -> str:
        """
        Translate Malayalam text to English
        
        Args:
            text: Malayalam text to translate
            
        Returns:
            English translation or original text if already English
        """
        detection = self.detect(text)
        
        if detection['language'] == 'ml':
            try:
                translated = self.translator.translate(text, src='ml', dest='en')
                return translated.text
            except:
                # Fallback: transliterate common terms
                return self._transliterate_malayalam(text)
        
        return text
    
    def translate_to_malayalam(self, text: str) -> str:
        """
        Translate English text to Malayalam
        
        Args:
            text: English text to translate
            
        Returns:
            Malayalam translation
        """
        try:
            translated = self.translator.translate(text, src='en', dest='ml')
            return translated.text
        except:
            return text
    
    def _transliterate_malayalam(self, text: str) -> str:
        """
        Basic transliteration of common Malayalam terms
        
        Args:
            text: Malayalam text
            
        Returns:
            Transliterated text
        """
        transliteration_map = {
            'ഹലോ': 'hello',
            'നമസ്കാരം': 'namaskaram',
            'സേവനങ്ങൾ': 'services',
            'വിവരങ്ങൾ': 'information',
            'ദസ്താവേജ്': 'document',
            'അപേക്ഷ': 'application',
            'സർട്ടിഫിക്കറ്റ്': 'certificate',
            'കാർഡ്': 'card',
            'രജിസ്ട്രേഷൻ': 'registration',
            'ജനനം': 'birth',
            'മരണം': 'death',
            'വിവാഹം': 'marriage',
            'പാസ്പോർട്ട്': 'passport',
            'പാൻ': 'pan',
            'ആധാർ': 'aadhaar',
            'റേഷൻ': 'ration',
            'പോലീസ്': 'police',
            'ഡോക്കുമെന്റ്': 'document',
            'ആവശ്യമാണ്': 'required',
            'എന്താണ്': 'what is',
            'എങ്ങനെ': 'how',
            'എവിടെ': 'where',
            'എപ്പോൾ': 'when'
        }
        
        for mal, eng in transliteration_map.items():
            text = text.replace(mal, eng)
        
        return text
    
    def get_service_in_language(self, service_key: str, language: str) -> str:
        """
        Get service name in specified language
        
        Args:
            service_key: Service identifier
            language: Target language ('en' or 'ml')
            
        Returns:
            Service name in target language
        """
        service_names = {
            'ration_card': {'en': 'Ration Card Services', 'ml': 'റേഷൻ കാർഡ് സേവനങ്ങൾ'},
            'marriage_registration': {'en': 'Marriage Registration', 'ml': 'വിവാഹ രജിസ്ട്രേഷൻ'},
            'police_clearance': {'en': 'Police Clearance Certificate', 'ml': 'പോലീസ് ക്ലിയറൻസ് സർട്ടിഫിക്കറ്റ്'},
            'pan_card': {'en': 'PAN Card Services', 'ml': 'പാൻ കാർഡ് സേവനങ്ങൾ'},
            'birth_certificate': {'en': 'Birth Certificate Services', 'ml': 'ജനന സർട്ടിഫിക്കറ്റ് സേവനങ്ങൾ'},
            'passport': {'en': 'Passport Services', 'ml': 'പാസ്പോർട്ട് സേവനങ്ങൾ'},
            'aadhaar': {'en': 'Aadhaar Services', 'ml': 'ആധാർ സേവനങ്ങൾ'},
            'death_registration': {'en': 'Death Registration Services', 'ml': 'മരണ രജിസ്ട്രേഷൻ സേവനങ്ങൾ'},
            'ncl_certificate': {'en': 'Non-Creamy Layer Certificate', 'ml': 'നോൺ ക്രീം ലെയർ സർട്ടിഫിക്കറ്റ്'}
        }
        
        return service_names.get(service_key, {}).get(language, service_key)