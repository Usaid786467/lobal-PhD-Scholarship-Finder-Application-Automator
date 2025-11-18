"""
Matching Engine
Calculates compatibility between users and professors
"""
import json
import logging
from typing import Dict, List
from .gemini_service import GeminiService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MatchingEngine:
    """Calculates match scores between applicants and professors"""

    def __init__(self, gemini_service: GeminiService):
        """
        Initialize matching engine
        Args:
            gemini_service: Configured GeminiService instance
        """
        self.gemini = gemini_service

    def calculate_match_score(self, user_interests: str, professor_interests: str) -> float:
        """
        Calculate match score between user and professor
        Args:
            user_interests: User's research interests (JSON string or text)
            professor_interests: Professor's research interests (JSON string or text)
        Returns:
            Match score (0-100)
        """
        try:
            # Use Gemini AI for intelligent matching
            match_result = self.gemini.analyze_research_match(user_interests, professor_interests)
            return float(match_result.get('score', 50))

        except Exception as e:
            logger.error(f"Error calculating match score: {str(e)}")
            # Fallback to keyword matching
            return self._keyword_match(user_interests, professor_interests)

    def _keyword_match(self, user_interests: str, professor_interests: str) -> float:
        """
        Fallback keyword-based matching
        Args:
            user_interests: User's research interests
            professor_interests: Professor's research interests
        Returns:
            Match score (0-100)
        """
        try:
            # Parse JSON if needed
            if isinstance(user_interests, str) and user_interests.startswith('['):
                user_keywords = set(json.loads(user_interests))
            else:
                user_keywords = set(user_interests.lower().split())

            if isinstance(professor_interests, str) and professor_interests.startswith('['):
                prof_keywords = set(json.loads(professor_interests))
            else:
                prof_keywords = set(professor_interests.lower().split())

            # Calculate Jaccard similarity
            if not user_keywords or not prof_keywords:
                return 50.0

            intersection = user_keywords.intersection(prof_keywords)
            union = user_keywords.union(prof_keywords)

            if not union:
                return 50.0

            score = (len(intersection) / len(union)) * 100
            return min(max(score, 0), 100)  # Clamp between 0-100

        except Exception as e:
            logger.error(f"Error in keyword matching: {str(e)}")
            return 50.0

    def batch_match_professors(self, user_interests: str, professors: List[Dict]) -> List[Dict]:
        """
        Calculate match scores for multiple professors
        Args:
            user_interests: User's research interests
            professors: List of professor dictionaries
        Returns:
            Professors with added match_score field, sorted by score
        """
        logger.info(f"Calculating match scores for {len(professors)} professors")

        for professor in professors:
            prof_interests = professor.get('research_interests', '[]')
            score = self.calculate_match_score(user_interests, prof_interests)
            professor['match_score'] = score

        # Sort by match score (highest first)
        professors.sort(key=lambda x: x.get('match_score', 0), reverse=True)

        logger.info(f"Match scores calculated. Top score: {professors[0].get('match_score', 0) if professors else 0}")
        return professors
