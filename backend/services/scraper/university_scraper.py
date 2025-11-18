"""
University Scraper for PhD Application Automator
Discovers universities and PhD programs worldwide
"""

from .base_scraper import BaseScraper
from models import get_session, University
from services.ai.gemini_service import get_gemini_service
import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class UniversityScraper(BaseScraper):
    """Scraper for discovering universities and PhD programs"""

    # Major universities database (starter list for each country)
    SEED_UNIVERSITIES = {
        'USA': [
            ('https://web.mit.edu', 'Massachusetts Institute of Technology', 'Cambridge', 'MA'),
            ('https://www.stanford.edu', 'Stanford University', 'Stanford', 'CA'),
            ('https://www.berkeley.edu', 'University of California, Berkeley', 'Berkeley', 'CA'),
            ('https://www.caltech.edu', 'California Institute of Technology', 'Pasadena', 'CA'),
            ('https://www.gatech.edu', 'Georgia Institute of Technology', 'Atlanta', 'GA'),
        ],
        'UK': [
            ('https://www.cam.ac.uk', 'University of Cambridge', 'Cambridge', ''),
            ('https://www.ox.ac.uk', 'University of Oxford', 'Oxford', ''),
            ('https://www.imperial.ac.uk', 'Imperial College London', 'London', ''),
            ('https://www.ucl.ac.uk', 'University College London', 'London', ''),
        ],
        'Canada': [
            ('https://www.utoronto.ca', 'University of Toronto', 'Toronto', 'ON'),
            ('https://www.ubc.ca', 'University of British Columbia', 'Vancouver', 'BC'),
            ('https://www.mcgill.ca', 'McGill University', 'Montreal', 'QC'),
        ],
        'Germany': [
            ('https://www.tum.de', 'Technical University of Munich', 'Munich', ''),
            ('https://www.rwth-aachen.de', 'RWTH Aachen University', 'Aachen', ''),
        ],
        'China': [
            ('https://www.tsinghua.edu.cn', 'Tsinghua University', 'Beijing', ''),
            ('https://www.pku.edu.cn', 'Peking University', 'Beijing', ''),
        ],
        'Singapore': [
            ('https://www.nus.edu.sg', 'National University of Singapore', 'Singapore', ''),
            ('https://www.ntu.edu.sg', 'Nanyang Technological University', 'Singapore', ''),
        ],
        'Australia': [
            ('https://www.unimelb.edu.au', 'University of Melbourne', 'Melbourne', 'VIC'),
            ('https://www.sydney.edu.au', 'University of Sydney', 'Sydney', 'NSW'),
        ],
    }

    def __init__(self):
        super().__init__(use_selenium=False)
        self.gemini = get_gemini_service()
        self.session_db = get_session()

    def discover_universities(self, countries: List[str] = None) -> List[Dict]:
        """
        Discover universities in specified countries

        Args:
            countries: List of country names (or None for all)

        Returns:
            List of university data dictionaries
        """
        if countries is None:
            countries = list(self.SEED_UNIVERSITIES.keys())

        discovered = []

        for country in countries:
            logger.info(f"Discovering universities in {country}")

            # Use seed universities for this country
            if country in self.SEED_UNIVERSITIES:
                for url, name, city, state in self.SEED_UNIVERSITIES[country]:
                    try:
                        uni_data = self.scrape_university(url, name, country, city, state)
                        if uni_data:
                            discovered.append(uni_data)
                            self._save_university(uni_data)
                    except Exception as e:
                        logger.error(f"Error scraping {name}: {str(e)}")
                        continue

        logger.info(f"Discovered {len(discovered)} universities")
        return discovered

    def scrape_university(
        self,
        url: str,
        name: str,
        country: str,
        city: str = "",
        state: str = ""
    ) -> Optional[Dict]:
        """
        Scrape detailed information about a university

        Args:
            url: University website URL
            name: University name
            country: Country name
            city: City name
            state: State/province (if applicable)

        Returns:
            Dictionary of university data
        """
        try:
            logger.info(f"Scraping university: {name}")

            # Check robots.txt
            if not self.respect_robots_txt(url):
                logger.warning(f"Scraping not allowed by robots.txt: {url}")
                return None

            # Fetch homepage
            html = self.fetch_page(url)
            if not html:
                logger.warning(f"Could not fetch page: {url}")
                return None

            soup = self.parse_html(html)

            # Extract basic information
            domain = self.get_base_url(url).replace('https://', '').replace('http://', '')

            # Try to find engineering/mechanical engineering department
            dept_url = self._find_engineering_department(soup, url)

            # Try to find graduate admissions page
            admissions_url = self._find_admissions_page(soup, url)

            # Look for scholarship information
            scholarship_info = self._find_scholarship_info(soup, url)

            # Build university data
            uni_data = {
                'name': name,
                'country': country,
                'city': city,
                'state_province': state,
                'website': url,
                'domain': domain,
                'department_url': dept_url,
                'application_url': admissions_url,
                'has_scholarship': bool(scholarship_info),
                'scholarship_details': scholarship_info.get('details', '') if scholarship_info else '',
                'scholarship_url': scholarship_info.get('url', '') if scholarship_info else '',
                'language_of_instruction': 'English',  # Default, can be enhanced
                'accepts_international': True,  # Default, can be enhanced
                'last_scraped': datetime.utcnow(),
                'scraping_status': 'completed',
                'source_url': url
            }

            # If we found department page, scrape more details
            if dept_url:
                dept_data = self._scrape_department_page(dept_url)
                uni_data.update(dept_data)

            return uni_data

        except Exception as e:
            logger.error(f"Error scraping {name}: {str(e)}")
            return None

    def _find_engineering_department(self, soup, base_url: str) -> Optional[str]:
        """Find mechanical/aerospace engineering department URL"""
        keywords = [
            'mechanical engineering',
            'aerospace engineering',
            'engineering department',
            'school of engineering'
        ]

        # Look for links containing keywords
        for a_tag in self.safe_find_all(soup, 'a', href=True):
            text = a_tag.get_text().lower()
            href = a_tag['href']

            for keyword in keywords:
                if keyword in text:
                    from urllib.parse import urljoin
                    return urljoin(base_url, href)

        return None

    def _find_admissions_page(self, soup, base_url: str) -> Optional[str]:
        """Find graduate admissions page"""
        keywords = [
            'graduate admissions',
            'phd admissions',
            'apply',
            'graduate programs',
            'doctoral programs'
        ]

        for a_tag in self.safe_find_all(soup, 'a', href=True):
            text = a_tag.get_text().lower()
            href = a_tag['href']

            for keyword in keywords:
                if keyword in text:
                    from urllib.parse import urljoin
                    return urljoin(base_url, href)

        return None

    def _find_scholarship_info(self, soup, base_url: str) -> Optional[Dict]:
        """Find scholarship/funding information"""
        keywords = [
            'scholarship',
            'funding',
            'fellowship',
            'financial aid',
            'stipend',
            'tuition waiver'
        ]

        # Search page text for scholarship mentions
        page_text = soup.get_text().lower()

        for keyword in keywords:
            if keyword in page_text:
                # Try to find specific scholarship page
                for a_tag in self.safe_find_all(soup, 'a', href=True):
                    if keyword in a_tag.get_text().lower():
                        from urllib.parse import urljoin
                        return {
                            'details': f'{keyword.title()} available',
                            'url': urljoin(base_url, a_tag['href'])
                        }

                return {
                    'details': f'{keyword.title()} mentioned on website',
                    'url': base_url
                }

        return None

    def _scrape_department_page(self, url: str) -> Dict:
        """Scrape department page for additional details"""
        data = {}

        try:
            html = self.fetch_page(url)
            if not html:
                return data

            soup = self.parse_html(html)

            # Extract research areas
            research_areas = self._extract_research_areas(soup)
            if research_areas:
                data['research_areas'] = research_areas

            # Extract contact info
            emails = self.extract_emails(soup.get_text())
            if emails:
                data['contact_email'] = emails[0]

        except Exception as e:
            logger.warning(f"Error scraping department page: {str(e)}")

        return data

    def _extract_research_areas(self, soup) -> List[str]:
        """Extract research areas from department page"""
        research_areas = []

        # Look for sections with research keywords
        keywords = ['research', 'areas', 'focus', 'topics']

        for heading in soup.find_all(['h2', 'h3', 'h4']):
            heading_text = heading.get_text().lower()

            if any(kw in heading_text for kw in keywords):
                # Get text from following elements
                next_elem = heading.find_next()
                if next_elem:
                    text = self.extract_text_from_element(next_elem)
                    # Use Gemini to extract research areas from text
                    areas = self.gemini.extract_research_interests_from_text(text)
                    research_areas.extend(areas)

        return list(set(research_areas))[:10]  # Unique, max 10

    def _save_university(self, uni_data: Dict):
        """Save university to database"""
        try:
            # Check if university already exists
            existing = self.session_db.query(University).filter_by(
                domain=uni_data['domain']
            ).first()

            if existing:
                # Update existing record
                for key, value in uni_data.items():
                    if hasattr(existing, key) and value:
                        setattr(existing, key, value)
                logger.info(f"Updated university: {uni_data['name']}")
            else:
                # Create new record
                university = University(**uni_data)
                self.session_db.add(university)
                logger.info(f"Added new university: {uni_data['name']}")

            self.session_db.commit()

        except Exception as e:
            logger.error(f"Error saving university: {str(e)}")
            self.session_db.rollback()

    def search_universities_by_keyword(self, keyword: str, country: str = None) -> List[str]:
        """
        Search for universities using search engines (placeholder)

        In production, this would use Google/Bing API or web search
        For now, returns empty list
        """
        # TODO: Implement search engine integration
        logger.info(f"Searching for universities: {keyword} in {country}")
        return []


# Example usage
if __name__ == '__main__':
    scraper = UniversityScraper()

    # Discover universities in USA
    universities = scraper.discover_universities(['USA'])

    for uni in universities:
        print(f"Found: {uni['name']} - {uni['country']}")
        print(f"  Scholarship: {uni['has_scholarship']}")
        print()
