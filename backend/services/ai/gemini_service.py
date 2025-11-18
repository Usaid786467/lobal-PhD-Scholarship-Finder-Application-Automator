"""
Google Gemini AI service for text generation and analysis
"""
import google.generativeai as genai
from typing import Dict, List, Optional
import time
from config import Config
from services.utils.logger import ai_logger


class GeminiService:
    """Service class for interacting with Google Gemini AI"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini service

        Args:
            api_key: Gemini API key (optional, will use config if not provided)
        """
        self.api_key = api_key or Config.GEMINI_API_KEY

        if not self.api_key:
            raise ValueError("Gemini API key is required")

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # Initialize model
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds between requests

        ai_logger.info("Gemini service initialized")

    def _rate_limit(self):
        """Apply rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def generate_text(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """
        Generate text using Gemini AI

        Args:
            prompt: Input prompt
            max_retries: Maximum number of retries

        Returns:
            Generated text or None
        """
        for attempt in range(max_retries):
            try:
                self._rate_limit()

                response = self.model.generate_content(prompt)

                if response and response.text:
                    ai_logger.info(f"Successfully generated text (length: {len(response.text)})")
                    return response.text

                ai_logger.warning(f"Empty response from Gemini (attempt {attempt + 1}/{max_retries})")

            except Exception as e:
                ai_logger.error(f"Error generating text (attempt {attempt + 1}/{max_retries}): {str(e)}")

                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff

        return None

    def generate_email(
        self,
        professor_name: str,
        professor_research: List[str],
        professor_publications: List[str],
        university_name: str,
        user_name: str,
        user_background: str,
        user_research_interests: List[str]
    ) -> Optional[Dict[str, str]]:
        """
        Generate personalized email for professor

        Args:
            professor_name: Professor's name
            professor_research: Professor's research interests
            professor_publications: Professor's recent publications
            university_name: University name
            user_name: User's name
            user_background: User's background
            user_research_interests: User's research interests

        Returns:
            Dictionary with 'subject' and 'body' or None
        """
        prompt = f"""
Generate a professional email to Professor {professor_name} at {university_name} expressing interest in their PhD program.

Professor's Research Interests:
{', '.join(professor_research)}

Recent Publications:
{', '.join(professor_publications[:3]) if professor_publications else 'Not available'}

My Background:
{user_background}

My Research Interests:
{', '.join(user_research_interests)}

Requirements:
1. Subject line: Concise and professional (max 80 characters)
2. Email body: 200-300 words
3. Professional and respectful tone
4. Mention specific research alignment
5. Reference at least one of their research interests or publications
6. Highlight my relevant experience
7. Include clear request for PhD opportunities and funding information
8. End with appropriate closing

Format the response as:
SUBJECT: [subject line]
BODY: [email body]
"""

        try:
            response_text = self.generate_text(prompt)

            if not response_text:
                return None

            # Parse response
            lines = response_text.strip().split('\n')
            subject = ''
            body = ''
            current_section = None

            for line in lines:
                line = line.strip()

                if line.startswith('SUBJECT:'):
                    subject = line.replace('SUBJECT:', '').strip()
                    current_section = 'subject'
                elif line.startswith('BODY:'):
                    body = line.replace('BODY:', '').strip()
                    current_section = 'body'
                elif current_section == 'body' and line:
                    body += '\n' + line

            # Clean up
            subject = subject.strip()
            body = body.strip()

            if not subject or not body:
                ai_logger.error("Failed to parse email from Gemini response")
                return None

            ai_logger.info(f"Generated email for {professor_name}")

            return {
                'subject': subject,
                'body': body
            }

        except Exception as e:
            ai_logger.error(f"Error generating email: {str(e)}")
            return None

    def extract_research_interests(self, text: str) -> List[str]:
        """
        Extract research interests from text

        Args:
            text: Text to analyze

        Returns:
            List of research interests
        """
        prompt = f"""
Analyze the following text and extract the main research interests or areas of expertise.
Return a comma-separated list of research topics (maximum 5-7 topics).

Text:
{text}

Return only the comma-separated list, nothing else.
"""

        try:
            response_text = self.generate_text(prompt)

            if not response_text:
                return []

            # Parse comma-separated list
            interests = [interest.strip() for interest in response_text.split(',')]
            interests = [interest for interest in interests if interest]

            ai_logger.info(f"Extracted {len(interests)} research interests")

            return interests[:7]  # Limit to 7

        except Exception as e:
            ai_logger.error(f"Error extracting research interests: {str(e)}")
            return []

    def calculate_research_match_score(
        self,
        user_interests: List[str],
        professor_interests: List[str]
    ) -> int:
        """
        Calculate match score between user and professor research interests

        Args:
            user_interests: User's research interests
            professor_interests: Professor's research interests

        Returns:
            Match score (0-100)
        """
        prompt = f"""
Calculate the research compatibility score between these two research interest profiles.

User's Research Interests:
{', '.join(user_interests)}

Professor's Research Interests:
{', '.join(professor_interests)}

Provide a compatibility score from 0-100, where:
- 90-100: Excellent match, highly aligned research areas
- 70-89: Good match, several overlapping areas
- 50-69: Moderate match, some common interests
- 30-49: Limited match, few overlapping areas
- 0-29: Poor match, minimal overlap

Return only the numerical score (0-100), nothing else.
"""

        try:
            response_text = self.generate_text(prompt)

            if not response_text:
                return 0

            # Extract number from response
            import re
            numbers = re.findall(r'\d+', response_text)

            if numbers:
                score = int(numbers[0])
                score = max(0, min(100, score))  # Clamp to 0-100

                ai_logger.info(f"Calculated match score: {score}")

                return score

            return 0

        except Exception as e:
            ai_logger.error(f"Error calculating match score: {str(e)}")
            return 0

    def analyze_scholarship_info(self, text: str) -> Dict[str, any]:
        """
        Analyze scholarship information from text

        Args:
            text: Text containing scholarship information

        Returns:
            Dictionary with scholarship details
        """
        prompt = f"""
Analyze the following text and extract scholarship information.

Text:
{text}

Extract:
1. Is scholarship/funding available? (yes/no)
2. Scholarship amount (if mentioned)
3. Application deadline (if mentioned)
4. Requirements (brief summary)

Format as JSON:
{{
    "available": true/false,
    "amount": "amount or null",
    "deadline": "deadline or null",
    "requirements": "requirements or null"
}}

Return only the JSON, nothing else.
"""

        try:
            response_text = self.generate_text(prompt)

            if not response_text:
                return {}

            # Parse JSON response
            import json
            import re

            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)

            if json_match:
                scholarship_info = json.loads(json_match.group())
                ai_logger.info("Successfully analyzed scholarship info")
                return scholarship_info

            return {}

        except Exception as e:
            ai_logger.error(f"Error analyzing scholarship info: {str(e)}")
            return {}

    def summarize_publications(self, publications: List[str], max_count: int = 3) -> str:
        """
        Summarize professor's publications

        Args:
            publications: List of publication titles
            max_count: Maximum number of publications to include

        Returns:
            Summary text
        """
        if not publications:
            return "No recent publications available."

        pubs_text = '\n'.join(publications[:max_count])

        prompt = f"""
Summarize the following research publications in 1-2 sentences,
highlighting the main research focus or themes.

Publications:
{pubs_text}

Provide a brief summary (1-2 sentences).
"""

        try:
            response_text = self.generate_text(prompt)

            if response_text:
                ai_logger.info("Successfully summarized publications")
                return response_text.strip()

            return pubs_text

        except Exception as e:
            ai_logger.error(f"Error summarizing publications: {str(e)}")
            return pubs_text


# Create singleton instance
gemini_service = GeminiService()
