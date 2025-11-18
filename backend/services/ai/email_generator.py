"""
Email Generator
Generates personalized emails using Gemini AI
"""
import json
import logging
from typing import Dict, Optional
from .gemini_service import GeminiService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailGenerator:
    """Generates personalized PhD application emails"""

    def __init__(self, gemini_service: GeminiService):
        """
        Initialize email generator
        Args:
            gemini_service: Configured GeminiService instance
        """
        self.gemini = gemini_service

    def generate_email(
        self,
        professor_name: str,
        professor_research: str,
        university_name: str,
        user_name: str,
        user_research: str,
        user_background: str = "Master's student in Mechanical Engineering"
    ) -> Dict[str, str]:
        """
        Generate personalized email
        Args:
            professor_name: Professor's name
            professor_research: Professor's research interests (JSON or text)
            university_name: University name
            user_name: Applicant's name
            user_research: Applicant's research interests
            user_background: Applicant's background
        Returns:
            Dictionary with 'subject' and 'body'
        """
        try:
            # Parse professor research if JSON
            if isinstance(professor_research, str) and professor_research.startswith('['):
                research_list = json.loads(professor_research)
                professor_research = ', '.join(research_list)

            prompt = f"""
Generate a professional PhD application email to a professor.

Professor: {professor_name}
University: {university_name}
Professor's Research: {professor_research}

Applicant: {user_name}
Applicant Background: {user_background}
Applicant Research Interests: {user_research}

Requirements:
1. Subject line: Concise and professional
2. Email body: 200-300 words
3. Mention specific research alignment with professor's work
4. Express genuine interest in their research
5. Briefly mention relevant background
6. Request consideration for PhD position
7. Professional and respectful tone
8. Mention CV is attached

Format:
SUBJECT: [subject line]

BODY:
[email body]

Generate the email now.
"""

            response = self.gemini.generate_content(prompt)

            if response:
                return self._parse_email_response(response)
            else:
                # Fallback to template
                return self._generate_template_email(
                    professor_name,
                    professor_research,
                    university_name,
                    user_name,
                    user_research
                )

        except Exception as e:
            logger.error(f"Error generating email: {str(e)}")
            return self._generate_template_email(
                professor_name,
                professor_research,
                university_name,
                user_name,
                user_research
            )

    def _parse_email_response(self, response: str) -> Dict[str, str]:
        """Parse Gemini email response"""
        try:
            parts = response.split('BODY:', 1)

            subject = 'PhD Application - Research Opportunity'
            body = response

            if len(parts) == 2:
                subject_part = parts[0].replace('SUBJECT:', '').strip()
                if subject_part:
                    subject = subject_part

                body = parts[1].strip()

            return {
                'subject': subject,
                'body': body
            }

        except Exception as e:
            logger.error(f"Error parsing email response: {str(e)}")
            return {
                'subject': 'PhD Application - Research Opportunity',
                'body': response
            }

    def _generate_template_email(
        self,
        professor_name: str,
        professor_research: str,
        university_name: str,
        user_name: str,
        user_research: str
    ) -> Dict[str, str]:
        """Generate template-based email as fallback"""

        subject = f"PhD Application - {user_research.split(',')[0] if ',' in user_research else 'Research Opportunity'}"

        body = f"""Dear Professor {professor_name},

I hope this email finds you well. I am writing to express my strong interest in pursuing a PhD position under your supervision at {university_name}.

I am currently completing my Master's degree in Mechanical Engineering, with a focus on {user_research}. I have been following your research in {professor_research}, and I am particularly impressed by your contributions to the field.

My research background aligns closely with your work, particularly in the areas of machine learning and advanced manufacturing. I believe that working under your guidance would provide an excellent opportunity to contribute meaningfully to your research group while advancing my academic goals.

I have attached my CV for your review. I would be grateful for the opportunity to discuss potential PhD positions in your lab. Thank you for considering my application.

Best regards,
{user_name}"""

        return {
            'subject': subject,
            'body': body
        }

    def batch_generate_emails(
        self,
        professors: list,
        user_name: str,
        user_research: str,
        user_background: str
    ) -> list:
        """
        Generate emails for multiple professors
        Args:
            professors: List of professor dictionaries
            user_name: Applicant name
            user_research: Applicant research interests
            user_background: Applicant background
        Returns:
            List of dictionaries with professor info and generated email
        """
        logger.info(f"Generating {len(professors)} emails")

        results = []
        for professor in professors:
            email = self.generate_email(
                professor_name=professor.get('name', 'Professor'),
                professor_research=professor.get('research_interests', ''),
                university_name=professor.get('university_name', 'University'),
                user_name=user_name,
                user_research=user_research,
                user_background=user_background
            )

            results.append({
                'professor': professor,
                'email': email
            })

        logger.info(f"Generated {len(results)} emails")
        return results
