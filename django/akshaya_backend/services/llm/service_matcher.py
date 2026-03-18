"""
Service matching module for user queries
"""
from typing import List, Dict, Any, Optional
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from ..models import Service, ServiceCategory
from .language_detector import LanguageDetector

class ServiceMatcher:
    """
    Matches user queries to relevant services
    """
    
    def __init__(self):
        """Initialize service matcher"""
        self.language_detector = LanguageDetector()
        self.services = None
        self.service_descriptions = None
        self.vectorizer = None
        self.tfidf_matrix = None
        
        self._load_services()
    
    def _load_services(self):
        """Load services from database"""
        self.services = list(Service.objects.filter(is_active=True))
        self.service_descriptions = []
        
        for service in self.services:
            # Create searchable text for each service
            search_text = f"{service.name} {service.description} {service.detailed_description} {service.service_type} {service.department}"
            self.service_descriptions.append(search_text.lower())
        
        # Initialize TF-IDF vectorizer
        if self.service_descriptions:
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(self.service_descriptions)
    
    def match(self, query: str, language: str = 'en', top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Match query to relevant services
        
        Args:
            query: User query
            language: Query language
            top_n: Number of top matches to return
            
        Returns:
            List of matched services with scores
        """
        if not self.services:
            return []
        
        # Translate query to English for matching
        if language == 'ml':
            query = self.language_detector.translate_to_english(query)
        
        # Convert query to searchable text
        query_text = query.lower()
        
        # Calculate similarities using multiple methods
        results = []
        
        for i, service in enumerate(self.services):
            # Calculate TF-IDF similarity
            tfidf_similarity = self._calculate_tfidf_similarity(query_text, i)
            
            # Calculate string similarity
            string_similarity = self._calculate_string_similarity(query_text, service)
            
            # Calculate keyword matching
            keyword_score = self._calculate_keyword_score(query_text, service)
            
            # Combine scores (weighted average)
            combined_score = (
                0.4 * tfidf_similarity +
                0.3 * string_similarity +
                0.3 * keyword_score
            )
            
            # Adjust score based on service popularity
            popularity_factor = min(1.0, service.popularity / 1000)
            final_score = combined_score * (1 + 0.1 * popularity_factor)
            
            if final_score > 0.1:  # Threshold to filter out irrelevant matches
                results.append({
                    'service': service,
                    'score': final_score,
                    'tfidf_similarity': tfidf_similarity,
                    'string_similarity': string_similarity,
                    'keyword_score': keyword_score
                })
        
        # Sort by score and return top_n
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # Prepare response
        matched_services = []
        for result in results[:top_n]:
            service = result['service']
            matched_services.append({
                'id': service.id,
                'name': service.name,
                'service_type': service.service_type,
                'description': service.description[:100] + '...',
                'score': round(result['score'], 3),
                'slug': service.slug,
                'department': service.department,
                'fee': float(service.fee),
                'processing_time': service.processing_time,
                'online_available': service.online_available
            })
        
        return matched_services
    
    def _calculate_tfidf_similarity(self, query: str, service_index: int) -> float:
        """
        Calculate TF-IDF similarity between query and service
        
        Args:
            query: User query
            service_index: Index of service in services list
            
        Returns:
            Similarity score (0 to 1)
        """
        try:
            query_vector = self.vectorizer.transform([query])
            service_vector = self.tfidf_matrix[service_index]
            
            similarity = cosine_similarity(query_vector, service_vector)
            return float(similarity[0][0])
        except:
            return 0.0
    
    def _calculate_string_similarity(self, query: str, service: Service) -> float:
        """
        Calculate string similarity using SequenceMatcher
        
        Args:
            query: User query
            service: Service object
            
        Returns:
            Similarity score (0 to 1)
        """
        # Compare with service name
        name_similarity = SequenceMatcher(None, query, service.name.lower()).ratio()
        
        # Compare with service type
        type_similarity = SequenceMatcher(None, query, service.service_type.replace('_', ' ')).ratio()
        
        # Compare with department
        dept_similarity = SequenceMatcher(None, query, service.department.lower()).ratio()
        
        return max(name_similarity, type_similarity, dept_similarity)
    
    def _calculate_keyword_score(self, query: str, service: Service) -> float:
        """
        Calculate keyword matching score
        
        Args:
            query: User query
            service: Service object
            
        Returns:
            Keyword score (0 to 1)
        """
        # Service-specific keywords
        keyword_sets = {
            'ration_card': ['ration', 'food', 'card', 'family', 'subsidy'],
            'marriage_registration': ['marriage', 'wedding', 'certificate', 'registration', 'spouse'],
            'police_clearance': ['police', 'clearance', 'pcc', 'character', 'certificate'],
            'pan_card': ['pan', 'card', 'permanent', 'account', 'number', 'income'],
            'birth_certificate': ['birth', 'certificate', 'born', 'date', 'child'],
            'passport': ['passport', 'travel', 'visa', 'country', 'international'],
            'aadhaar': ['aadhaar', 'uid', 'unique', 'identity', 'biometric'],
            'death_registration': ['death', 'certificate', 'demise', 'died', 'mortality'],
            'ncl_certificate': ['ncl', 'non', 'creamy', 'layer', 'caste', 'certificate']
        }
        
        keywords = keyword_sets.get(service.service_type, [])
        
        if not keywords:
            return 0.0
        
        # Count keyword matches
        matches = 0
        query_words = set(query.split())
        
        for keyword in keywords:
            if keyword in query_words:
                matches += 1
        
        return matches / len(keywords)
    
    def match_by_category(self, category_name: str, language: str = 'en') -> List[Dict[str, Any]]:
        """
        Match services by category
        
        Args:
            category_name: Category name
            language: Language for response
            
        Returns:
            List of services in category
        """
        try:
            category = ServiceCategory.objects.get(name__icontains=category_name, is_active=True)
            services = Service.objects.filter(category=category, is_active=True)
            
            result = []
            for service in services:
                result.append({
                    'id': service.id,
                    'name': service.name,
                    'service_type': service.service_type,
                    'description': service.description[:100] + '...',
                    'slug': service.slug,
                    'department': service.department,
                    'fee': float(service.fee),
                    'processing_time': service.processing_time,
                    'online_available': service.online_available
                })
            
            return result
        except ServiceCategory.DoesNotExist:
            return []
    
    def get_service_by_type(self, service_type: str) -> Optional[Dict[str, Any]]:
        """
        Get service by service type
        
        Args:
            service_type: Service type identifier
            
        Returns:
            Service information or None
        """
        try:
            service = Service.objects.get(service_type=service_type, is_active=True)
            
            return {
                'id': service.id,
                'name': service.name,
                'service_type': service.service_type,
                'description': service.description,
                'detailed_description': service.detailed_description,
                'slug': service.slug,
                'department': service.department,
                'fee': float(service.fee),
                'processing_time': service.processing_time,
                'online_available': service.online_available,
                'offline_centers': service.offline_centers,
                'steps': [
                    {
                        'step_number': step.step_number,
                        'title': step.title,
                        'description': step.description,
                        'estimated_time': step.estimated_time,
                        'is_online': step.is_online
                    }
                    for step in service.steps.all().order_by('step_number')
                ]
            }
        except Service.DoesNotExist:
            return None
    
    def get_popular_services(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get popular services based on popularity score
        
        Args:
            limit: Number of services to return
            
        Returns:
            List of popular services
        """
        services = Service.objects.filter(is_active=True).order_by('-popularity')[:limit]
        
        result = []
        for service in services:
            result.append({
                'id': service.id,
                'name': service.name,
                'service_type': service.service_type,
                'description': service.description[:100] + '...',
                'popularity': service.popularity,
                'slug': service.slug,
                'department': service.department,
                'fee': float(service.fee),
                'processing_time': service.processing_time
            })
        
        return result
    
    def refresh_services(self):
        """Refresh service cache from database"""
        self._load_services()