"""
Gemini AI Service
Core integration with Google Gemini API
"""
import google.generativeai as genai
import logging
from typing import Optional, Dict
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini AI"""

    def __init__(self, api_key: str):
        """
        Initialize Gemini service
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.retry_count = 3
        self.retry_delay = 2

    def generate_content(self, prompt: str, max_retries: Optional[int] = None) -> Optional[str]:
        """
        Generate content using Gemini
        Args:
            prompt: Input prompt
            max_retries: Maximum number of retries (default: 3)
        Returns:
            Generated text or None on failure
        """
        retries = max_retries if max_retries is not None else self.retry_count

        for attempt in range(retries):
            try:
                logger.info(f"Generating content with Gemini (attempt {attempt + 1}/{retries})")
                response = self.model.generate_content(prompt)

                if response and response.text:
                    return response.text

            except Exception as e:
                logger.error(f"Gemini API error (attempt {attempt + 1}): {str(e)}")
                if attempt < retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    logger.error("Max retries reached for Gemini API")

        return None

    def analyze_research_match(self, user_interests: str, professor_interests: str) -> Dict:
        """
        Analyze research compatibility between user and professor
        Args:
            user_interests: User's research interests (JSON string or text)
            professor_interests: Professor's research interests (JSON string or text)
        Returns:
            Dictionary with match score and analysis
        """
        prompt = f"""
Analyze the research compatibility between a PhD applicant and a professor.

Applicant's Research Interests:
{user_interests}

Professor's Research Interests:
{professor_interests}

Provide:
1. A compatibility score from 0-100 (where 100 is perfect match)
2. Key matching areas
3. Potential collaboration opportunities
4. A brief explanation

Format your response as:
SCORE: [number]
MATCHING_AREAS: [comma-separated list]
OPPORTUNITIES: [brief description]
EXPLANATION: [1-2 sentences]
"""

        try:
            response = self.generate_content(prompt)
            if response:
                return self._parse_match_response(response)
            return self._default_match_score()

        except Exception as e:
            logger.error(f"Error analyzing research match: {str(e)}")
            return self._default_match_score()

    def _parse_match_response(self, response: str) -> Dict:
        """Parse Gemini response for match analysis"""
        try:
            lines = response.strip().split('\n')
            result = {
                'score': 0,
                'matching_areas': [],
                'opportunities': '',
                'explanation': ''
            }

            for line in lines:
                if line.startswith('SCORE:'):
                    score_str = line.replace('SCORE:', '').strip()
                    # Extract number from string
                    import re
                    numbers = re.findall(r'\d+', score_str)
                    if numbers:
                        result['score'] = min(int(numbers[0]), 100)

                elif line.startswith('MATCHING_AREAS:'):
                    areas = line.replace('MATCHING_AREAS:', '').strip()
                    result['matching_areas'] = [a.strip() for a in areas.split(',')]

                elif line.startswith('OPPORTUNITIES:'):
                    result['opportunities'] = line.replace('OPPORTUNITIES:', '').strip()

                elif line.startswith('EXPLANATION:'):
                    result['explanation'] = line.replace('EXPLANATION:', '').strip()

            return result

        except Exception as e:
            logger.error(f"Error parsing match response: {str(e)}")
            return self._default_match_score()

    def _default_match_score(self) -> Dict:
        """Return default match score when API fails"""
        return {
            'score': 50,
            'matching_areas': ['General Engineering'],
            'opportunities': 'Potential collaboration in engineering research',
            'explanation': 'Match analysis based on general compatibility'
        }
