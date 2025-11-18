"""
Matching Engine Service
AI-powered matching between users and professors/universities
"""

import logging
from typing import List, Dict, Optional
from .gemini_service import get_gemini_service

logger = logging.getLogger(__name__)


class MatchingEngine:
    """Match users with professors and universities based on research interests"""

    def __init__(self):
        """Initialize matching engine"""
        self.gemini = get_gemini_service()
        logger.info("Matching engine initialized")

    def calculate_match_score(
        self,
        user_interests: List[str],
        professor_interests: List[str],
        professor_publications: List[Dict] = None
    ) -> Optional[Dict]:
        """
        Calculate match score between user and professor

        Args:
            user_interests: User's research interests
            professor_interests: Professor's research interests
            professor_publications: Professor's recent publications (optional)

        Returns:
            Dictionary with 'score' (0-100) and 'reasons' (list of match reasons)
        """
        try:
            # Format interests
            user_text = ", ".join(user_interests) if user_interests else ""
            prof_text = ", ".join(professor_interests) if professor_interests else ""

            # Add publications context if available
            pub_text = ""
            if professor_publications:
                pub_titles = [pub.get('title', '') for pub in professor_publications[:5]]
                pub_text = f"\nProfessor's recent publications: {', '.join(pub_titles)}"

            prompt = f"""
Analyze the research alignment between a PhD applicant and a professor.

APPLICANT'S RESEARCH INTERESTS:
{user_text}

PROFESSOR'S RESEARCH INTERESTS:
{prof_text}{pub_text}

Please provide:
1. A match score from 0-100 (where 0 is no alignment and 100 is perfect alignment)
2. List of specific reasons why they match or don't match
3. Potential collaboration areas

Respond in this JSON format:
{{
  "score": 85,
  "reasons": [
    "Both focus on deep learning applications",
    "Shared interest in manufacturing optimization"
  ],
  "collaboration_areas": [
    "Machine learning in aerospace",
    "Predictive maintenance systems"
  ],
  "concerns": [
    "Professor's work may be more theoretical"
  ]
}}

Respond with ONLY valid JSON.
"""

            response = self.gemini.generate_text(prompt, max_tokens=500)

            if response:
                try:
                    import json
                    result = json.loads(response)

                    # Validate score is in range
                    if 'score' in result:
                        result['score'] = max(0, min(100, result['score']))

                    logger.info(f"Match score calculated: {result.get('score', 0)}")
                    return result

                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse match score JSON: {str(e)}")
                    # Fallback to basic text similarity
                    return self._fallback_matching(user_interests, professor_interests)

            return None

        except Exception as e:
            logger.error(f"Error calculating match score: {str(e)}")
            return self._fallback_matching(user_interests, professor_interests)

    def _fallback_matching(
        self,
        user_interests: List[str],
        professor_interests: List[str]
    ) -> Dict:
        """Simple fallback matching based on keyword overlap"""
        try:
            # Convert to lowercase for comparison
            user_set = set([i.lower() for i in user_interests])
            prof_set = set([i.lower() for i in professor_interests])

            # Calculate overlap
            overlap = user_set.intersection(prof_set)
            overlap_count = len(overlap)

            # Calculate score (0-100)
            total = len(user_set.union(prof_set))
            score = (overlap_count / total * 100) if total > 0 else 0

            reasons = []
            if overlap_count > 0:
                reasons.append(f"Shared interests: {', '.join(overlap)}")
            else:
                reasons.append("No direct overlap in research interests")

            return {
                'score': round(score, 2),
                'reasons': reasons,
                'collaboration_areas': list(overlap),
                'concerns': []
            }

        except Exception as e:
            logger.error(f"Fallback matching failed: {str(e)}")
            return {
                'score': 50.0,
                'reasons': ['Unable to calculate precise match'],
                'collaboration_areas': [],
                'concerns': []
            }

    def rank_professors(
        self,
        user_interests: List[str],
        professors: List[Dict]
    ) -> List[Dict]:
        """
        Rank a list of professors by match score

        Args:
            user_interests: User's research interests
            professors: List of professor dictionaries with 'id' and 'research_interests'

        Returns:
            Sorted list of professors with added 'match_score' and 'match_reasons'
        """
        try:
            ranked = []

            for prof in professors:
                prof_interests = prof.get('research_interests', [])
                prof_pubs = prof.get('publications', [])

                # Calculate match score
                match_result = self.calculate_match_score(
                    user_interests,
                    prof_interests,
                    prof_pubs
                )

                if match_result:
                    prof['match_score'] = match_result.get('score', 0)
                    prof['match_reasons'] = match_result.get('reasons', [])
                    prof['collaboration_areas'] = match_result.get('collaboration_areas', [])
                else:
                    prof['match_score'] = 0
                    prof['match_reasons'] = []
                    prof['collaboration_areas'] = []

                ranked.append(prof)

            # Sort by match score (highest first)
            ranked.sort(key=lambda x: x.get('match_score', 0), reverse=True)

            logger.info(f"Ranked {len(ranked)} professors")
            return ranked

        except Exception as e:
            logger.error(f"Error ranking professors: {str(e)}")
            return professors

    def extract_research_interests(self, text: str) -> List[str]:
        """
        Extract research interests from text (e.g., professor bio, publication list)

        Args:
            text: Text to analyze

        Returns:
            List of research interests/keywords
        """
        try:
            prompt = f"""
Extract the main research interests and areas from this text.
Focus on technical topics, methodologies, and application domains.

TEXT:
{text[:2000]}  # Limit text length

Return ONLY a JSON array of research interests/keywords, like:
["Deep Learning", "Computer Vision", "Manufacturing", "Quality Control"]

Respond with ONLY valid JSON array.
"""

            response = self.gemini.generate_text(prompt, max_tokens=300)

            if response:
                try:
                    import json
                    interests = json.loads(response)

                    if isinstance(interests, list):
                        return interests[:15]  # Limit to 15 interests

                except json.JSONDecodeError:
                    logger.error("Failed to parse research interests JSON")

            return []

        except Exception as e:
            logger.error(f"Error extracting research interests: {str(e)}")
            return []

    def suggest_research_topics(
        self,
        user_interests: List[str],
        professor_interests: List[str]
    ) -> List[str]:
        """
        Suggest potential research topics based on shared interests

        Args:
            user_interests: User's research interests
            professor_interests: Professor's research interests

        Returns:
            List of suggested research topics
        """
        try:
            user_text = ", ".join(user_interests)
            prof_text = ", ".join(professor_interests)

            prompt = f"""
Based on these two sets of research interests, suggest 5 potential PhD research topics
that would align well with both parties.

APPLICANT'S INTERESTS:
{user_text}

PROFESSOR'S INTERESTS:
{prof_text}

Return as JSON array of specific, actionable research topics:
["Topic 1", "Topic 2", ...]

Respond with ONLY valid JSON array.
"""

            response = self.gemini.generate_text(prompt, max_tokens=400)

            if response:
                try:
                    import json
                    topics = json.loads(response)

                    if isinstance(topics, list):
                        return topics[:10]

                except json.JSONDecodeError:
                    logger.error("Failed to parse research topics JSON")

            return []

        except Exception as e:
            logger.error(f"Error suggesting research topics: {str(e)}")
            return []


# Create singleton instance
_matching_engine = None


def get_matching_engine() -> MatchingEngine:
    """Get singleton matching engine instance"""
    global _matching_engine

    if _matching_engine is None:
        _matching_engine = MatchingEngine()

    return _matching_engine
