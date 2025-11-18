"""
Base Scraper for PhD Application Automator
Foundation for all web scraping operations
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import logging
from typing import Optional, Dict, List
from config import Config

logger = logging.getLogger(__name__)


class BaseScraper:
    """Base class for all scrapers"""

    def __init__(self, use_selenium=False):
        """
        Initialize scraper

        Args:
            use_selenium: Whether to use Selenium for JavaScript rendering
        """
        self.use_selenium = use_selenium
        self.session = requests.Session()
        self.driver = None

        # Configuration
        self.user_agent = Config.USER_AGENT
        self.delay = Config.SCRAPING_DELAY
        self.timeout = Config.TIMEOUT
        self.max_retries = Config.MAX_RETRIES

        # Setup session headers
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

        logger.info(f"Base scraper initialized (Selenium: {use_selenium})")

    def get_selenium_driver(self):
        """Initialize and return Selenium WebDriver"""
        if self.driver:
            return self.driver

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=chrome_options)
        logger.info("Selenium driver initialized")
        return self.driver

    def fetch_page(self, url: str, method='GET', data=None, use_selenium=False) -> Optional[str]:
        """
        Fetch webpage content

        Args:
            url: URL to fetch
            method: HTTP method (GET or POST)
            data: POST data if applicable
            use_selenium: Force use of Selenium for this request

        Returns:
            HTML content or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetching: {url} (attempt {attempt + 1}/{self.max_retries})")

                if use_selenium or self.use_selenium:
                    return self._fetch_with_selenium(url)
                else:
                    return self._fetch_with_requests(url, method, data)

            except Exception as e:
                logger.warning(f"Fetch attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay * (attempt + 1))  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
                    return None

        return None

    def _fetch_with_requests(self, url: str, method='GET', data=None) -> str:
        """Fetch using requests library"""
        if method == 'GET':
            response = self.session.get(url, timeout=self.timeout)
        else:
            response = self.session.post(url, data=data, timeout=self.timeout)

        response.raise_for_status()
        time.sleep(self.delay)  # Respectful delay

        return response.text

    def _fetch_with_selenium(self, url: str) -> str:
        """Fetch using Selenium (for JavaScript-heavy pages)"""
        driver = self.get_selenium_driver()
        driver.get(url)

        # Wait for page to load
        WebDriverWait(driver, self.timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Additional wait for JavaScript
        time.sleep(2)

        html = driver.page_source
        time.sleep(self.delay)  # Respectful delay

        return html

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content

        Args:
            html: HTML string

        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, 'lxml')

    def extract_emails(self, text: str) -> List[str]:
        """
        Extract email addresses from text

        Args:
            text: Text to search for emails

        Returns:
            List of email addresses
        """
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # Remove duplicates

    def extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers from text"""
        import re
        # Simple pattern for international phone numbers
        phone_pattern = r'\+?[\d\s\-\(\)]{10,}'
        phones = re.findall(phone_pattern, text)
        return [p.strip() for p in phones if len(p.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) >= 10]

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove extra whitespace
        text = ' '.join(text.split())

        # Remove special characters
        text = text.replace('\xa0', ' ')
        text = text.replace('\n', ' ')
        text = text.replace('\t', ' ')

        return text.strip()

    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        import re
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None

    def get_base_url(self, url: str) -> str:
        """Extract base URL from full URL"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Selenium driver closed")

        if self.session:
            self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def respect_robots_txt(self, url: str) -> bool:
        """
        Check if scraping is allowed by robots.txt

        Args:
            url: URL to check

        Returns:
            True if allowed, False otherwise
        """
        try:
            from urllib.robotparser import RobotFileParser
            from urllib.parse import urlparse

            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()

            return rp.can_fetch(self.user_agent, url)

        except Exception as e:
            logger.warning(f"Could not check robots.txt for {url}: {str(e)}")
            # If we can't check, assume it's allowed (but be respectful with delays)
            return True

    def extract_links(self, soup: BeautifulSoup, base_url: str, filter_pattern=None) -> List[str]:
        """
        Extract links from page

        Args:
            soup: BeautifulSoup object
            base_url: Base URL for relative links
            filter_pattern: Regex pattern to filter links

        Returns:
            List of URLs
        """
        from urllib.parse import urljoin
        import re

        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)

            if self.is_valid_url(full_url):
                if filter_pattern:
                    if re.search(filter_pattern, full_url):
                        links.append(full_url)
                else:
                    links.append(full_url)

        return list(set(links))  # Remove duplicates

    def extract_text_from_element(self, element) -> str:
        """Extract and clean text from BeautifulSoup element"""
        if element:
            return self.clean_text(element.get_text())
        return ""

    def safe_find(self, soup, *args, **kwargs):
        """Safely find element (returns None if not found)"""
        try:
            return soup.find(*args, **kwargs)
        except:
            return None

    def safe_find_all(self, soup, *args, **kwargs):
        """Safely find all elements (returns empty list if not found)"""
        try:
            return soup.find_all(*args, **kwargs)
        except:
            return []
