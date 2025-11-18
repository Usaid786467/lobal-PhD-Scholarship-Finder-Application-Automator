"""
Gemini AI Service for PhD Application Automator
Handles AI-powered email generation, matching, and content analysis
"""

import google.generativeai as genai
from config import Config
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini AI"""

    def __init__(self):
        """Initialize Gemini AI with API key"""
        self.api_key = Config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in configuration")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self.temperature = Config.GEMINI_TEMPERATURE
        self.max_tokens = Config.GEMINI_MAX_TOKENS

        logger.info("Gemini AI service initialized successfully")

    def generate_personalized_email(
        self,
        professor_name: str,
        professor_research: List[str],
        professor_recent_papers: List[Dict],
        university_name: str,
        user_name: str,
        user_background: str,
        user_research_interests: List[str],
        **kwargs
    ) -> Dict[str, str]:
        """
        Generate personalized email to professor

        Args:
            professor_name: Professor's full name
            professor_research: List of research interests
            professor_recent_papers: List of recent publications
            university_name: University name
            user_name: Applicant's name
            user_background: Applicant's background/degree
            user_research_interests: Applicant's research interests
            **kwargs: Additional context

        Returns:
            Dict with 'subject' and 'body'
        """
        try:
            # Build prompt for Gemini
            prompt = self._build_email_prompt(
                professor_name=professor_name,
                professor_research=professor_research,
                professor_recent_papers=professor_recent_papers,
                university_name=university_name,
                user_name=user_name,
                user_background=user_background,
                user_research_interests=user_research_interests,
                **kwargs
            )

            # Generate email using Gemini
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )

            # Parse response
            email_content = response.text
            subject, body = self._parse_email_response(email_content)

            logger.info(f"Generated email for {professor_name}")

            return {
                'subject': subject,
                'body': body,
                'word_count': len(body.split())
            }

        except Exception as e:
            logger.error(f"Error generating email: {str(e)}")
            # Return fallback template
            return self._fallback_email_template(
                professor_name, university_name, user_name
            )

    def _build_email_prompt(
        self,
        professor_name: str,
        professor_research: List[str],
        professor_recent_papers: List[Dict],
        university_name: str,
        user_name: str,
        user_background: str,
        user_research_interests: List[str],
        **kwargs
    ) -> str:
        """Build prompt for email generation"""

        # Format research interests
        prof_research_str = ", ".join(professor_research[:5]) if professor_research else "Not specified"
        user_research_str = ", ".join(user_research_interests[:5]) if user_research_interests else "Not specified"

        # Format recent papers (top 3)
        papers_str = ""
        if professor_recent_papers:
            papers = professor_recent_papers[:3]
            papers_str = "\n".join([
                f"- {paper.get('title', 'Untitled')} ({paper.get('year', 'N/A')})"
                for paper in papers
            ])
        else:
            papers_str = "No recent publications available"

        prompt = f"""
You are an expert at writing professional, personalized PhD application emails.

Generate a personalized email to Professor {professor_name} at {university_name} expressing interest in their PhD program.

PROFESSOR'S RESEARCH INTERESTS:
{prof_research_str}

PROFESSOR'S RECENT PUBLICATIONS:
{papers_str}

APPLICANT'S PROFILE:
Name: {user_name}
Background: {user_background}
Research Interests: {user_research_str}

REQUIREMENTS:
1. Subject line: Concise and professional (max 60 characters)
2. Email body: 200-300 words
3. Professional and respectful tone
4. Mention specific overlap in research interests
5. Reference at least one of the professor's recent papers (if available)
6. Highlight applicant's relevant experience or skills
7. Express genuine interest in joining their research group
8. Ask about PhD openings and funding opportunities
9. Include a clear call-to-action
10. Do NOT use excessive flattery or generic statements
11. Be specific and authentic

IMPORTANT GUIDELINES:
- Focus on research alignment and mutual benefits
- Demonstrate knowledge of the professor's work
- Be concise and respectful of their time
- Maintain professional academic tone
- Avoid clichés like "I am writing to express my keen interest"
- Start with a strong, specific opening

FORMAT YOUR RESPONSE AS:
SUBJECT: [Your subject line here]

BODY:
[Your email body here]

Generate the email now:
"""

        return prompt

    def _parse_email_response(self, response_text: str) -> tuple:
        """Parse Gemini response to extract subject and body"""
        lines = response_text.strip().split('\n')

        subject = ""
        body_lines = []
        body_started = False

        for line in lines:
            if line.startswith('SUBJECT:'):
                subject = line.replace('SUBJECT:', '').strip()
            elif line.startswith('BODY:'):
                body_started = True
            elif body_started and line.strip():
                body_lines.append(line.strip())

        # If parsing failed, try alternative parsing
        if not subject or not body_lines:
            # Look for first line as subject, rest as body
            if len(lines) > 1:
                subject = lines[0].replace('Subject:', '').replace('SUBJECT:', '').strip()
                body_lines = [l.strip() for l in lines[1:] if l.strip()]

        body = '\n\n'.join(body_lines)

        # Fallback subject if still empty
        if not subject:
            subject = "PhD Application Inquiry"

        return subject, body

    def _fallback_email_template(
        self,
        professor_name: str,
        university_name: str,
        user_name: str
    ) -> Dict[str, str]:
        """Fallback email template if AI generation fails"""
        subject = f"PhD Application Inquiry - {user_name}"

        body = f"""Dear Professor {professor_name},

I am writing to inquire about potential PhD opportunities in your research group at {university_name}.

I hold a Master's degree in Mechanical Engineering and have research experience in Deep Learning and Machine Learning applications in aerospace manufacturing. Your work aligns closely with my research interests, and I would be honored to contribute to your research group.

I am particularly interested in exploring opportunities in your lab and would appreciate the chance to discuss potential research directions and funding availability.

I have attached my CV for your review. Thank you for considering my application.

Best regards,
{user_name}"""

        return {'subject': subject, 'body': body, 'word_count': len(body.split())}

    def calculate_research_match(
        self,
        professor_interests: List[str],
        user_interests: List[str],
        professor_keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        Calculate research alignment score using AI

        Returns:
            Dict with score (0-100) and matching topics
        """
        try:
            if not professor_interests or not user_interests:
                return {'score': 0, 'matches': [], 'explanation': 'Insufficient data'}

            prof_str = ", ".join(professor_interests)
            user_str = ", ".join(user_interests)

            prompt = f"""
Analyze the research alignment between a PhD applicant and a professor.

PROFESSOR'S RESEARCH INTERESTS:
{prof_str}

APPLICANT'S RESEARCH INTERESTS:
{user_str}

Provide:
1. A compatibility score from 0-100 (100 = perfect match)
2. List of overlapping research areas
3. Brief explanation of the match

Respond in this exact format:
SCORE: [number]
MATCHES: [topic1, topic2, topic3]
EXPLANATION: [brief explanation]
"""

            response = self.model.generate_content(prompt)
            result = self._parse_match_response(response.text)

            logger.info(f"Calculated match score: {result['score']}")
            return result

        except Exception as e:
            logger.error(f"Error calculating match: {str(e)}")
            # Fallback to simple keyword matching
            return self._simple_keyword_match(professor_interests, user_interests)

    def _parse_match_response(self, response_text: str) -> Dict:
        """Parse match calculation response"""
        lines = response_text.strip().split('\n')

        score = 0
        matches = []
        explanation = ""

        for line in lines:
            if line.startswith('SCORE:'):
                try:
                    score = int(line.replace('SCORE:', '').strip())
                except:
                    score = 50
            elif line.startswith('MATCHES:'):
                matches_str = line.replace('MATCHES:', '').strip()
                matches = [m.strip() for m in matches_str.split(',')]
            elif line.startswith('EXPLANATION:'):
                explanation = line.replace('EXPLANATION:', '').strip()

        return {
            'score': min(max(score, 0), 100),  # Clamp between 0-100
            'matches': matches[:5],  # Top 5 matches
            'explanation': explanation
        }

    def _simple_keyword_match(
        self,
        prof_interests: List[str],
        user_interests: List[str]
    ) -> Dict:
        """Simple keyword-based matching as fallback"""
        prof_lower = [p.lower() for p in prof_interests]
        user_lower = [u.lower() for u in user_interests]

        matches = []
        for user_int in user_lower:
            for prof_int in prof_lower:
                if user_int in prof_int or prof_int in user_int:
                    matches.append(user_int)
                    break

        score = min(len(matches) * 25, 100)  # 25 points per match, max 100

        return {
            'score': score,
            'matches': matches[:5],
            'explanation': f'Found {len(matches)} overlapping research areas'
        }

    def extract_research_interests_from_text(self, text: str) -> List[str]:
        """Extract research interests from unstructured text"""
        try:
            prompt = f"""
Extract research interests and topics from the following text.
Provide a list of 5-10 specific research areas.

TEXT:
{text[:2000]}  # Limit text length

Return only a comma-separated list of research topics.
"""

            response = self.model.generate_content(prompt)
            interests = [i.strip() for i in response.text.split(',')]

            return interests[:10]  # Return top 10

        except Exception as e:
            logger.error(f"Error extracting research interests: {str(e)}")
            return []

    def summarize_professor_research(
        self,
        publications: List[Dict],
        research_interests: List[str]
    ) -> str:
        """Generate brief research summary for professor"""
        try:
            pubs_str = "\n".join([
                f"- {pub.get('title', 'N/A')}"
                for pub in publications[:5]
            ])

            interests_str = ", ".join(research_interests[:10])

            prompt = f"""
Create a brief 2-3 sentence summary of this professor's research focus.

RESEARCH INTERESTS:
{interests_str}

RECENT PUBLICATIONS:
{pubs_str}

Provide a concise, professional summary:
"""

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Error summarizing research: {str(e)}")
            return f"Research focus: {', '.join(research_interests[:5])}"


# Global instance
_gemini_service = None


def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance"""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
