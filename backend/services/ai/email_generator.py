"""
Email Generator Service
AI-powered personalized email generation for PhD applications
"""

import logging
from typing import Optional, Dict, List
from .gemini_service import get_gemini_service

logger = logging.getLogger(__name__)


class EmailGenerator:
    """Generate personalized emails for PhD applications"""

    def __init__(self):
        """Initialize email generator"""
        self.gemini = get_gemini_service()
        logger.info("Email generator initialized")

    def generate_email(
        self,
        professor_name: str,
        professor_interests: List[str],
        professor_publications: List[Dict] = None,
        university_name: str = "",
        department: str = "",
        user_background: str = "",
        user_interests: List[str] = None,
        custom_message: str = "",
        tone: str = "professional"
    ) -> Optional[Dict[str, str]]:
        """
        Generate a personalized email for a professor

        Args:
            professor_name: Name of the professor
            professor_interests: List of professor's research interests
            professor_publications: Recent publications (optional)
            university_name: University name
            department: Department name
            user_background: User's background and experience
            user_interests: User's research interests
            custom_message: Custom message to include
            tone: Email tone (professional, friendly, formal)

        Returns:
            Dictionary with 'subject' and 'body' or None if failed
        """
        try:
            # Build the prompt for Gemini
            prompt = self._build_email_prompt(
                professor_name=professor_name,
                professor_interests=professor_interests,
                professor_publications=professor_publications,
                university_name=university_name,
                department=department,
                user_background=user_background,
                user_interests=user_interests or [],
                custom_message=custom_message,
                tone=tone
            )

            # Generate email using Gemini
            response = self.gemini.generate_text(prompt, max_tokens=1000)

            if not response:
                logger.error("No response from Gemini")
                return None

            # Parse the response to extract subject and body
            email_parts = self._parse_email_response(response)

            if email_parts:
                logger.info(f"Email generated successfully for {professor_name}")
                return email_parts

            return None

        except Exception as e:
            logger.error(f"Error generating email: {str(e)}")
            return None

    def _build_email_prompt(
        self,
        professor_name: str,
        professor_interests: List[str],
        professor_publications: List[Dict],
        university_name: str,
        department: str,
        user_background: str,
        user_interests: List[str],
        custom_message: str,
        tone: str
    ) -> str:
        """Build the prompt for email generation"""

        # Format professor's research interests
        interests_text = ", ".join(professor_interests) if professor_interests else "various areas"

        # Format recent publications if available
        publications_text = ""
        if professor_publications and len(professor_publications) > 0:
            pub_list = []
            for pub in professor_publications[:3]:  # Use top 3 publications
                title = pub.get('title', '')
                year = pub.get('year', '')
                if title:
                    pub_list.append(f"- {title} ({year})")
            if pub_list:
                publications_text = f"\n\nRecent publications:\n" + "\n".join(pub_list)

        # Format user interests
        user_interests_text = ", ".join(user_interests) if user_interests else "machine learning and deep learning"

        # Build the comprehensive prompt
        prompt = f"""
Generate a professional email to a professor expressing interest in their PhD program.

PROFESSOR INFORMATION:
- Name: Professor {professor_name}
- University: {university_name}
- Department: {department}
- Research Interests: {interests_text}{publications_text}

APPLICANT INFORMATION:
- Background: {user_background if user_background else "Master's student in Mechanical Engineering with focus on Deep Learning and Machine Learning in Aerospace Manufacturing"}
- Research Interests: {user_interests_text}
- Skills: Model training, Manufacturing optimization, Computer vision, Predictive maintenance

REQUIREMENTS:
1. Email tone: {tone}
2. Length: 200-300 words
3. Structure:
   - Personalized introduction mentioning specific research alignment
   - Brief background (2-3 sentences)
   - Why their lab/research is interesting (specific reasons)
   - Mention of shared research interests
   - Polite request about PhD opportunities and funding
   - Professional closing

4. Include these elements:
   - Reference to their specific research area
   - Highlight research alignment
   - Show genuine interest in their work
   - Ask about PhD positions and funding availability

5. DO NOT:
   - Be generic or template-like
   - Use overly formal language
   - Make it too long
   - Make unverifiable claims

{f"6. Additional context to include: {custom_message}" if custom_message else ""}

Format the response as:
SUBJECT: [email subject line]

BODY:
[email body]

Generate the email now:
"""

        return prompt

    def _parse_email_response(self, response: str) -> Optional[Dict[str, str]]:
        """Parse Gemini response to extract subject and body"""
        try:
            lines = response.strip().split('\n')

            subject = ""
            body_lines = []
            found_subject = False
            found_body = False

            for line in lines:
                line = line.strip()

                # Look for subject
                if line.upper().startswith('SUBJECT:'):
                    subject = line.split(':', 1)[1].strip()
                    found_subject = True
                    continue

                # Look for body marker
                if line.upper().startswith('BODY:'):
                    found_body = True
                    continue

                # Collect body lines
                if found_body and line:
                    body_lines.append(line)
                elif found_subject and not found_body and line and ':' not in line:
                    # Sometimes body starts without explicit marker
                    body_lines.append(line)
                    found_body = True

            body = '\n\n'.join(body_lines).strip()

            # Validate we got both parts
            if subject and body:
                return {
                    'subject': subject,
                    'body': body
                }

            # Fallback: if parsing failed, use heuristics
            if not subject:
                subject = "PhD Opportunity - Research Collaboration"

            if not body and response:
                # Use the whole response as body if parsing failed
                body = response.replace('SUBJECT:', '').replace('BODY:', '').strip()

            if body:
                return {
                    'subject': subject,
                    'body': body
                }

            return None

        except Exception as e:
            logger.error(f"Error parsing email response: {str(e)}")
            return None

    def generate_follow_up_email(
        self,
        professor_name: str,
        original_email: str,
        days_since_sent: int,
        custom_message: str = ""
    ) -> Optional[Dict[str, str]]:
        """
        Generate a follow-up email

        Args:
            professor_name: Name of the professor
            original_email: The original email body
            days_since_sent: Number of days since original email
            custom_message: Additional context

        Returns:
            Dictionary with 'subject' and 'body' or None
        """
        try:
            prompt = f"""
Generate a polite follow-up email to Professor {professor_name}.

CONTEXT:
- Original email was sent {days_since_sent} days ago
- No response has been received yet
- Original email content:
{original_email[:500]}  # Include snippet of original

REQUIREMENTS:
1. Be polite and understanding
2. Brief reminder of previous email
3. Restate interest in the position
4. Ask if they need any additional information
5. Length: 100-150 words
6. Professional tone

{f"Additional context: {custom_message}" if custom_message else ""}

Format as:
SUBJECT: [subject]

BODY:
[body]
"""

            response = self.gemini.generate_text(prompt, max_tokens=500)

            if response:
                return self._parse_email_response(response)

            return None

        except Exception as e:
            logger.error(f"Error generating follow-up email: {str(e)}")
            return None

    def improve_email(self, email_body: str, improvements: str) -> Optional[str]:
        """
        Improve an existing email based on feedback

        Args:
            email_body: Original email body
            improvements: Requested improvements

        Returns:
            Improved email body or None
        """
        try:
            prompt = f"""
Improve this email based on the following feedback:

ORIGINAL EMAIL:
{email_body}

IMPROVEMENTS REQUESTED:
{improvements}

Please rewrite the email incorporating these improvements while maintaining:
- Professional tone
- Original intent
- Appropriate length (200-300 words)

Return only the improved email body (no subject line).
"""

            response = self.gemini.generate_text(prompt, max_tokens=800)

            return response

        except Exception as e:
            logger.error(f"Error improving email: {str(e)}")
            return None


# Create singleton instance
_email_generator = None


def get_email_generator() -> EmailGenerator:
    """Get singleton email generator instance"""
    global _email_generator

    if _email_generator is None:
        _email_generator = EmailGenerator()

    return _email_generator
