"""
Utility functions for Ama Arogya ChatBot
"""
import re
import time
from typing import List, Dict, Optional
from functools import lru_cache
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor response times and performance metrics"""

    @staticmethod
    def measure_time(func):
        """Decorator to measure function execution time"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = (end_time - start_time) * \
                1000  # Convert to milliseconds
            logger.info(f"{func.__name__} executed in {execution_time:.2f}ms")
            return result, execution_time
        return wrapper


class TextProcessor:
    """Enhanced text processing utilities"""

    @staticmethod
    @lru_cache(maxsize=1000)
    def normalize_text(text: str) -> str:
        """Normalize text for better matching (cached for performance)"""
        if not text:
            return ""

        # Convert to lowercase and remove extra whitespace
        text = re.sub(r'\s+', ' ', text.lower().strip())

        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.,\?!।॥]', '', text)

        return text

    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        """Extract keywords from text"""
        normalized = TextProcessor.normalize_text(text)
        # Split by common separators and filter out short words
        keywords = [word for word in re.split(r'[,\s]+', normalized)
                    if len(word) > 2]
        return list(set(keywords))  # Remove duplicates

    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calculate simple similarity between two texts"""
        words1 = set(TextProcessor.extract_keywords(text1))
        words2 = set(TextProcessor.extract_keywords(text2))

        if not words1 or not words2:
            return 0.0

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0


class HealthResponseGenerator:
    """Generate intelligent health responses"""

    def __init__(self):
        self.symptom_patterns = {
            'fever': [
                'fever', 'ज्वर', 'ଜ୍ବର', 'jwor', 'bukhar', 'temperature', 'hot'
            ],
            'headache': [
                'headache', 'सिरदर्द', 'ମାଥା ବଥା', 'matharu', 'batha', 'head', 'pain'
            ],
            'cough': [
                'cough', 'खांसी', 'କାଶ', 'khansi', 'kash', 'throat'
            ],
            'stomach_pain': [
                'stomach', 'पेट', 'ପେଟ', 'pet', 'abdomen', 'belly', 'pain', 'ache'
            ],
            'pregnancy': [
                'pregnancy', 'pregnant', 'गर्भावस्था', 'ଗର୍ଭାବସ୍ଥା', 'garbha', 'maternal'
            ],
            'vaccination': [
                'vaccination', 'vaccine', 'टीका', 'ଟୀକା', 'tika', 'immunization'
            ]
        }

        self.responses = {
            'fever': {
                'en': "For fever: Take adequate rest, stay hydrated with plenty of fluids, use cool compresses. If fever exceeds 102°F or persists for more than 3 days, consult a doctor immediately.",
                'hi': "बुखार के लिए: पर्याप्त आराम लें, पानी और तरल पदार्थों से हाइड्रेटेड रहें, ठंडी पट्टी का उपयोग करें। यदि बुखार 102°F से अधिक हो या 3 दिनों से अधिक बना रहे तो तुरंत डॉक्टर से संपर्क करें।",
                'or': "ଜ୍ବର ପାଇଁ: ଯଥେଷ୍ଟ ବିଶ୍ରାମ ନିଅନ୍ତୁ, ପାଣି ଏବଂ ତରଳ ପଦାର୍ଥ ପିଅନ୍ତୁ, ଥଣ୍ଡା ସେକ ବ୍ୟବହାର କରନ୍ତୁ। ଯଦି ଜ୍ବର 102°F ରୁ ଅଧିକ ହୁଏ କିମ୍ବା 3 ଦିନରୁ ଅଧିକ ରହେ ତେବେ ତୁରନ୍ତ ଡାକ୍ତରଙ୍କ ସହିତ ଯୋଗାଯୋଗ କରନ୍ତୁ।"
            },
            'headache': {
                'en': "For headache: Rest in a quiet, dark room. Apply cold or warm compress to head or neck. Stay hydrated. If severe or persistent, consult a healthcare provider.",
                'hi': "सिरदर्द के लिए: शांत, अंधेरे कमरे में आराम करें। सिर या गर्दन पर ठंडी या गर्म पट्टी लगाएं। हाइड्रेटेड रहें। यदि गंभीर या लगातार हो तो स्वास्थ्य सेवा प्रदाता से सलाह लें।",
                'or': "ମାଥା ବଥା ପାଇଁ: ଶାନ୍ତ, ଅନ୍ଧାର କୋଠରୀରେ ବିଶ୍ରାମ ନିଅନ୍ତୁ। ମୁଣ୍ଡ କିମ୍ବା ବେକରେ ଥଣ୍ଡା କିମ୍ବା ଗରମ ସେକ ଲଗାନ୍ତୁ। ହାଇଡ୍ରେଟେଡ୍ ରୁହନ୍ତୁ।"
            },
            'default': {
                'en': "I'm here to help with health-related questions. Please describe your symptoms or ask about health topics like vaccination, pregnancy care, or common illnesses.",
                'hi': "मैं स्वास्थ्य संबंधी प्रश्नों में मदद के लिए यहाँ हूँ। कृपया अपने लक्षणों का वर्णन करें या टीकाकरण, गर्भावस्था देखभाल, या सामान्य बीमारियों के बारे में पूछें।",
                'or': "ମୁଁ ସ୍ୱାସ୍ଥ୍ୟ ସମ୍ବନ୍ଧୀୟ ପ୍ରଶ୍ନରେ ସାହାଯ୍ୟ ପାଇଁ ଏଠାରେ ଅଛି। ଦୟାକରି ଆପଣଙ୍କର ଲକ୍ଷଣ ବର୍ଣ୍ଣନା କରନ୍ତୁ କିମ୍ବା ଟୀକାକରଣ, ଗର୍ଭାବସ୍ଥା ଯତ୍ନ, କିମ୍ବା ସାଧାରଣ ରୋଗ ବିଷୟରେ ପଚାରନ୍ତୁ।"
            }
        }

    def detect_topic(self, message: str) -> Optional[str]:
        """Detect health topic from message"""
        normalized_message = TextProcessor.normalize_text(message)

        for topic, patterns in self.symptom_patterns.items():
            for pattern in patterns:
                if pattern.lower() in normalized_message:
                    return topic

        return None

    def generate_response(self, message: str, language: str = 'en') -> tuple[str, str]:
        """Generate appropriate response based on message content"""
        topic = self.detect_topic(message)

        if topic and topic in self.responses:
            response = self.responses[topic].get(
                language, self.responses[topic]['en'])
            return response, topic
        else:
            response = self.responses['default'].get(
                language, self.responses['default']['en'])
            return response, 'general'


class ResponseCache:
    """Simple in-memory cache for responses"""

    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}

    def get(self, key: str) -> Optional[str]:
        """Get cached response"""
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None

    def set(self, key: str, value: str):
        """Set cached response"""
        if len(self.cache) >= self.max_size:
            # Remove least recently used item
            oldest_key = min(self.access_times.items(), key=lambda x: x[1])[0]
            del self.cache[oldest_key]
            del self.access_times[oldest_key]

        self.cache[key] = value
        self.access_times[key] = time.time()

    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.access_times.clear()


# Global instances
text_processor = TextProcessor()
health_response_generator = HealthResponseGenerator()
response_cache = ResponseCache()
performance_monitor = PerformanceMonitor()
