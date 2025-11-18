"""
Gemini AI Service
Integration with Google Gemini AI for various AI-powered features
"""

import os
import google.generativeai as genai
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini AI"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini service with API key"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        if not self.api_key:
            raise ValueError("Gemini API key not provided")

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # Initialize model
        self.model = genai.GenerativeModel('gemini-pro')

        logger.info("Gemini AI service initialized")

    def generate_text(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """
        Generate text using Gemini

        Args:
            prompt: The prompt to send to Gemini
            max_tokens: Maximum number of tokens to generate

        Returns:
            Generated text or None if failed
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7,
                )
            )

            if response and response.text:
                return response.text.strip()

            return None

        except Exception as e:
            logger.error(f"Error generating text with Gemini: {str(e)}")
            return None

    def analyze_text(self, text: str, analysis_type: str) -> Optional[Dict]:
        """
        Analyze text using Gemini

        Args:
            text: Text to analyze
            analysis_type: Type of analysis (sentiment, keywords, summary, etc.)

        Returns:
            Analysis results as dictionary
        """
        try:
            prompts = {
                'sentiment': f"Analyze the sentiment of this text and respond with JSON containing 'sentiment' (positive/negative/neutral) and 'confidence' (0-1):\n\n{text}",
                'keywords': f"Extract the main keywords and topics from this text. Return as JSON with a 'keywords' array:\n\n{text}",
                'summary': f"Provide a concise summary of this text in 2-3 sentences:\n\n{text}",
                'research_areas': f"Identify the research areas mentioned in this text. Return as JSON with a 'research_areas' array:\n\n{text}"
            }

            prompt = prompts.get(analysis_type)
            if not prompt:
                logger.error(f"Unknown analysis type: {analysis_type}")
                return None

            response = self.generate_text(prompt, max_tokens=500)

            if response:
                # Try to parse as JSON
                try:
                    import json
                    return json.loads(response)
                except:
                    return {'result': response}

            return None

        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            return None

    def extract_information(self, text: str, fields: List[str]) -> Optional[Dict]:
        """
        Extract specific information from text

        Args:
            text: Text to extract from
            fields: List of fields to extract (e.g., ['email', 'phone', 'name'])

        Returns:
            Dictionary with extracted fields
        """
        try:
            prompt = f"""
            Extract the following information from this text and return as JSON:
            Fields to extract: {', '.join(fields)}

            Text:
            {text}

            Return only valid JSON with the extracted fields. If a field is not found, use null.
            """

            response = self.generate_text(prompt, max_tokens=500)

            if response:
                try:
                    import json
                    return json.loads(response)
                except:
                    logger.warning("Could not parse extraction result as JSON")
                    return None

            return None

        except Exception as e:
            logger.error(f"Error extracting information: {str(e)}")
            return None

    def compare_texts(self, text1: str, text2: str) -> Optional[float]:
        """
        Compare two texts for similarity

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score (0-100) or None if failed
        """
        try:
            prompt = f"""
            Compare these two texts and rate their similarity on a scale of 0-100,
            where 0 is completely different and 100 is identical.
            Focus on semantic meaning and topic overlap.

            Text 1:
            {text1}

            Text 2:
            {text2}

            Respond with ONLY a number between 0 and 100.
            """

            response = self.generate_text(prompt, max_tokens=10)

            if response:
                try:
                    score = float(response.strip())
                    return max(0, min(100, score))  # Clamp between 0-100
                except:
                    logger.warning("Could not parse similarity score")
                    return None

            return None

        except Exception as e:
            logger.error(f"Error comparing texts: {str(e)}")
            return None

    def chat(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """
        Have a conversation with Gemini

        Args:
            messages: List of message dictionaries with 'role' and 'content'

        Returns:
            Response text or None
        """
        try:
            # Convert messages to prompt format
            prompt_parts = []
            for msg in messages:
                role = msg.get('role', 'user')
                content = msg.get('content', '')

                if role == 'user':
                    prompt_parts.append(f"User: {content}")
                elif role == 'assistant':
                    prompt_parts.append(f"Assistant: {content}")

            prompt = "\n\n".join(prompt_parts)

            return self.generate_text(prompt)

        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            return None


# Create a singleton instance
_gemini_service = None


def get_gemini_service() -> GeminiService:
    """Get singleton Gemini service instance"""
    global _gemini_service

    if _gemini_service is None:
        _gemini_service = GeminiService()

    return _gemini_service
