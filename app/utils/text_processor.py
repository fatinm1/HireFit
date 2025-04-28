import re
from typing import List, Dict
import json

class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:!?()]', '', text)
        return text.strip()

    @staticmethod
    def extract_json_from_text(text: str) -> Dict:
        """
        Extract JSON from text response
        """
        try:
            # Find JSON-like content in the text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            return {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """
        Split text into sentences
        """
        # Basic sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> List[str]:
        """
        Extract keywords from text
        """
        # Remove common words and short words
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if len(word) >= min_length]

    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Calculate basic text similarity using word overlap
        """
        words1 = set(TextProcessor.extract_keywords(text1))
        words2 = set(TextProcessor.extract_keywords(text2))
        
        if not words1 or not words2:
            return 0.0
            
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0 