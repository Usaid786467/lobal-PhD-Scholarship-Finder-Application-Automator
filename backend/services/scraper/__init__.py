"""
Scraper Services Package
Web scraping for universities and professors
"""
from .university_scraper import UniversityScraper
from .professor_scraper import ProfessorScraper

__all__ = ['UniversityScraper', 'ProfessorScraper']
