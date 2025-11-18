"""
Professor Scraper for PhD Application Automator
Discovers professor profiles and research information
"""

from .base_scraper import BaseScraper
from models import get_session, Professor, University
from services.ai.gemini_service import get_gemini_service
import logging
from datetime import datetime
from typing import List, Dict, Optional
import re

logger = logging.getLogger(__name__)


class ProfessorScraper(BaseScraper):
    """Scraper for discovering professor profiles"""

    def __init__(self):
        super().__init__(use_selenium=False)
        self.gemini = get_gemini_service()
        self.session_db = get_session()

    def discover_professors_at_university(self, university_id: int) -> List[Dict]:
        """
        Discover professors at a specific university

        Args:
            university_id: University database ID

        Returns:
            List of professor data dictionaries
        """
        university = self.session_db.query(University).filter_by(id=university_id).first()

        if not university:
            logger.error(f"University {university_id} not found")
            return []

        logger.info(f"Discovering professors at {university.name}")

        professors = []

        # Try department page first
        if university.department_url:
            profs = self._scrape_department_faculty(university.department_url, university_id)
            professors.extend(profs)

        logger.info(f"Discovered {len(professors)} professors at {university.name}")
        return professors

    def _scrape_department_faculty(self, dept_url: str, university_id: int) -> List[Dict]:
        """Scrape faculty list from department page"""
        professors = []

        try:
            html = self.fetch_page(dept_url)
            if not html:
                return professors

            soup = self.parse_html(html)

            # Look for faculty listings
            faculty_sections = soup.find_all(['div', 'section'], class_=re.compile(r'faculty|staff|people|team'))

            for section in faculty_sections:
                # Find individual faculty entries
                faculty_cards = section.find_all(['div', 'article', 'li'], class_=re.compile(r'faculty|profile|person'))

                for card in faculty_cards[:20]:  # Limit to 20 professors
                    prof_data = self._extract_professor_data(card, university_id, dept_url)
                    if prof_data:
                        professors.append(prof_data)
                        self._save_professor(prof_data)

        except Exception as e:
            logger.error(f"Error scraping faculty: {str(e)}")

        return professors

    def _extract_professor_data(self, element, university_id: int, base_url: str) -> Optional[Dict]:
        """Extract professor information from HTML element"""
        try:
            # Extract name
            name_elem = element.find(['h2', 'h3', 'h4', 'a'], class_=re.compile(r'name|title'))
            name = self.extract_text_from_element(name_elem) if name_elem else None

            if not name:
                return None

            # Extract email
            email = None
            email_link = element.find('a', href=re.compile(r'mailto:'))
            if email_link:
                email = email_link['href'].replace('mailto:', '')

            # Extract title/position
            title_elem = element.find(['span', 'p'], class_=re.compile(r'title|position|rank'))
            title = self.extract_text_from_element(title_elem) if title_elem else "Professor"

            # Extract profile URL
            profile_url = None
            profile_link = element.find('a', href=True)
            if profile_link:
                from urllib.parse import urljoin
                profile_url = urljoin(base_url, profile_link['href'])

            # Extract department
            dept_elem = element.find(['span', 'p'], class_=re.compile(r'department'))
            department = self.extract_text_from_element(dept_elem) if dept_elem else "Mechanical Engineering"

            prof_data = {
                'university_id': university_id,
                'name': name,
                'title': title,
                'email': email,
                'department': department,
                'profile_url': profile_url,
                'last_scraped': datetime.utcnow(),
                'scraping_status': 'completed'
            }

            # If we have profile URL, scrape more details
            if profile_url:
                details = self._scrape_professor_profile(profile_url)
                prof_data.update(details)

            return prof_data

        except Exception as e:
            logger.error(f"Error extracting professor data: {str(e)}")
            return None

    def _scrape_professor_profile(self, profile_url: str) -> Dict:
        """Scrape detailed professor profile"""
        data = {}

        try:
            html = self.fetch_page(profile_url)
            if not html:
                return data

            soup = self.parse_html(html)

            # Extract email if not already found
            emails = self.extract_emails(soup.get_text())
            if emails:
                data['email'] = emails[0]

            # Extract research interests
            research_text = ""
            research_section = soup.find(['div', 'section'], class_=re.compile(r'research|interest'))
            if research_section:
                research_text = self.extract_text_from_element(research_section)

            if research_text:
                interests = self.gemini.extract_research_interests_from_text(research_text)
                data['research_interests'] = interests
                data['research_summary'] = research_text[:500]

            # Look for Google Scholar link
            scholar_link = soup.find('a', href=re.compile(r'scholar.google'))
            if scholar_link:
                data['google_scholar_url'] = scholar_link['href']

            # Look for publications
            pub_section = soup.find(['div', 'section'], class_=re.compile(r'publication|paper'))
            if pub_section:
                pubs = []
                pub_items = pub_section.find_all(['li', 'div'], limit=10)
                for item in pub_items:
                    pub_text = self.extract_text_from_element(item)
                    if pub_text:
                        pubs.append({'title': pub_text})

                data['publications'] = pubs
                data['total_publications'] = len(pubs)

        except Exception as e:
            logger.warning(f"Error scraping professor profile: {str(e)}")

        return data

    def _save_professor(self, prof_data: Dict):
        """Save professor to database"""
        try:
            # Check if professor already exists
            existing = self.session_db.query(Professor).filter_by(
                university_id=prof_data['university_id'],
                name=prof_data['name']
            ).first()

            if existing:
                # Update existing
                for key, value in prof_data.items():
                    if hasattr(existing, key) and value:
                        setattr(existing, key, value)
                logger.info(f"Updated professor: {prof_data['name']}")
            else:
                # Create new
                professor = Professor(**prof_data)
                self.session_db.add(professor)
                logger.info(f"Added new professor: {prof_data['name']}")

            self.session_db.commit()

        except Exception as e:
            logger.error(f"Error saving professor: {str(e)}")
            self.session_db.rollback()
