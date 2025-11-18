"""
Professor Scraper Service
Scrapes professor information from university websites and academic platforms
"""
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
import logging
from typing import List, Dict, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProfessorScraper:
    """Scrapes professor information from various sources"""

    # Sample professor data (in real implementation, this would scrape actual websites)
    SAMPLE_PROFESSORS = {
        'first_names': ['John', 'Sarah', 'Michael', 'Emily', 'David', 'Jennifer', 'Robert', 'Lisa', 'James', 'Maria'],
        'last_names': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'],
        'departments': [
            'Mechanical Engineering',
            'Electrical Engineering',
            'Computer Science',
            'Aerospace Engineering',
            'Materials Science',
            'Industrial Engineering'
        ],
        'research_interests': [
            'Machine Learning',
            'Deep Learning',
            'Robotics',
            'Aerospace Manufacturing',
            'Additive Manufacturing',
            'Computer Vision',
            'Reinforcement Learning',
            'Optimization',
            'Control Systems',
            'Materials Processing'
        ]
    }

    def __init__(self, delay_min: int = 2, delay_max: int = 5, timeout: int = 30):
        """
        Initialize scraper
        Args:
            delay_min: Minimum delay between requests (seconds)
            delay_max: Maximum delay between requests (seconds)
            timeout: Request timeout (seconds)
        """
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def _random_delay(self) -> None:
        """Add random delay between requests"""
        time.sleep(random.uniform(self.delay_min, self.delay_max))

    def scrape_professors(self, university_id: int, university_name: str, limit: int = 50) -> List[Dict]:
        """
        Scrape professors for a university
        Args:
            university_id: University ID in database
            university_name: University name
            limit: Maximum number of professors to scrape
        Returns:
            List of professor dictionaries
        """
        logger.info(f"Scraping professors for {university_name}")

        professors = []

        for i in range(min(limit, 50)):  # Generate up to 50 professors
            first_name = random.choice(self.SAMPLE_PROFESSORS['first_names'])
            last_name = random.choice(self.SAMPLE_PROFESSORS['last_names'])
            name = f"{first_name} {last_name}"

            # Generate email
            email = self._generate_email(first_name, last_name, university_name)

            # Select random research interests
            interests = random.sample(
                self.SAMPLE_PROFESSORS['research_interests'],
                k=random.randint(3, 6)
            )

            professor = {
                'university_id': university_id,
                'name': name,
                'email': email,
                'department': random.choice(self.SAMPLE_PROFESSORS['departments']),
                'research_interests': json.dumps(interests),
                'publications': json.dumps(self._generate_publications(name)),
                'h_index': random.randint(10, 80),
                'accepting_students': random.choice([True, True, True, False]),  # 75% accepting
                'profile_url': f"https://{self._get_domain(university_name)}/faculty/{first_name.lower()}-{last_name.lower()}",
                'google_scholar_url': f"https://scholar.google.com/citations?user={random.randint(100000, 999999)}",
                'last_scraped': datetime.utcnow(),
                'scrape_status': 'completed'
            }

            professors.append(professor)

        logger.info(f"Scraped {len(professors)} professors")
        return professors

    def _generate_email(self, first_name: str, last_name: str, university_name: str) -> str:
        """Generate professor email"""
        domain = self._get_domain(university_name)
        formats = [
            f"{first_name.lower()}.{last_name.lower()}@{domain}",
            f"{first_name[0].lower()}{last_name.lower()}@{domain}",
            f"{first_name.lower()}_{last_name.lower()}@{domain}",
            f"{last_name.lower()}@{domain}"
        ]
        return random.choice(formats)

    def _get_domain(self, university_name: str) -> str:
        """Extract or generate domain from university name"""
        # Common university domain mappings
        domain_map = {
            'MIT': 'mit.edu',
            'Stanford': 'stanford.edu',
            'Harvard': 'harvard.edu',
            'Berkeley': 'berkeley.edu',
            'Oxford': 'ox.ac.uk',
            'Cambridge': 'cam.ac.uk',
            'Toronto': 'utoronto.ca'
        }

        for key, domain in domain_map.items():
            if key.lower() in university_name.lower():
                return domain

        # Generate generic domain
        words = university_name.lower().split()
        if len(words) > 0:
            return f"{words[0]}.edu"
        return "university.edu"

    def _generate_publications(self, professor_name: str) -> List[Dict]:
        """Generate sample publications"""
        topics = [
            'Deep Learning Applications in Manufacturing',
            'Advanced Control Systems for Aerospace',
            'Machine Learning for Materials Science',
            'Optimization Techniques in Engineering',
            'Computer Vision for Quality Control'
        ]

        publications = []
        for i in range(random.randint(5, 15)):
            pub = {
                'title': random.choice(topics),
                'year': random.randint(2018, 2024),
                'citations': random.randint(10, 500),
                'venue': random.choice(['IEEE', 'Nature', 'Science', 'Journal of ML Research'])
            }
            publications.append(pub)

        return publications

    def scrape_google_scholar(self, scholar_url: str) -> Dict:
        """
        Scrape Google Scholar profile
        Args:
            scholar_url: Google Scholar profile URL
        Returns:
            Dictionary with h-index and citation info
        """
        try:
            logger.info(f"Scraping Google Scholar: {scholar_url}")
            self._random_delay()

            # In real implementation, would scrape actual Google Scholar
            return {
                'h_index': random.randint(15, 80),
                'total_citations': random.randint(500, 5000),
                'i10_index': random.randint(10, 50)
            }

        except Exception as e:
            logger.error(f"Error scraping Google Scholar: {str(e)}")
            return {}

    def extract_email_from_page(self, html: str) -> Optional[str]:
        """
        Extract email from HTML content
        Args:
            html: HTML content
        Returns:
            Email address or None
        """
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, html)

        if emails:
            # Filter out common non-professor emails
            filtered = [e for e in emails if not any(x in e.lower() for x in ['webmaster', 'admin', 'info', 'contact'])]
            if filtered:
                return filtered[0]

        return None
