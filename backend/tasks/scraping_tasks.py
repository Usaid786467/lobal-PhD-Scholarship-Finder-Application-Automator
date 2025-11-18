"""
Scraping Tasks
Celery tasks for asynchronous web scraping
"""
from celery_app import celery
from services.scraper import UniversityScraper, ProfessorScraper
from models import db, University, Professor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery.task(bind=True, name='tasks.scrape_universities')
def scrape_universities_task(self, country=None, limit=50):
    """
    Celery task to scrape universities
    Args:
        country: Country filter (optional)
        limit: Maximum universities to scrape
    Returns:
        Dictionary with results
    """
    try:
        logger.info(f"Starting university scraping task for country: {country}")

        scraper = UniversityScraper()
        universities_data = scraper.scrape_universities(country=country, limit=limit)

        # Note: In a real Celery task, you'd need to handle database context properly
        # This is a simplified version
        saved_count = len(universities_data)

        logger.info(f"University scraping completed. Scraped {saved_count} universities")

        return {
            'status': 'success',
            'count': saved_count,
            'country': country
        }

    except Exception as e:
        logger.error(f"Error in university scraping task: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }


@celery.task(bind=True, name='tasks.scrape_professors')
def scrape_professors_task(self, university_id, university_name, limit=50):
    """
    Celery task to scrape professors
    Args:
        university_id: University ID
        university_name: University name
        limit: Maximum professors to scrape
    Returns:
        Dictionary with results
    """
    try:
        logger.info(f"Starting professor scraping task for {university_name}")

        scraper = ProfessorScraper()
        professors_data = scraper.scrape_professors(
            university_id=university_id,
            university_name=university_name,
            limit=limit
        )

        saved_count = len(professors_data)

        logger.info(f"Professor scraping completed. Scraped {saved_count} professors")

        return {
            'status': 'success',
            'count': saved_count,
            'university_id': university_id
        }

    except Exception as e:
        logger.error(f"Error in professor scraping task: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }
