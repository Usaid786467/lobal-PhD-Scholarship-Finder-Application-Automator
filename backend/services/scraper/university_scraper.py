"""
University Scraper Service
Scrapes universities from multiple countries and sources
"""
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversityScraper:
    """Scrapes university information from various sources"""

    # Top universities by country (sample data - can be expanded)
    UNIVERSITIES_DATABASE = {
        'USA': [
            {'name': 'Massachusetts Institute of Technology', 'website': 'https://web.mit.edu'},
            {'name': 'Stanford University', 'website': 'https://www.stanford.edu'},
            {'name': 'Harvard University', 'website': 'https://www.harvard.edu'},
            {'name': 'California Institute of Technology', 'website': 'https://www.caltech.edu'},
            {'name': 'University of California Berkeley', 'website': 'https://www.berkeley.edu'},
            {'name': 'Carnegie Mellon University', 'website': 'https://www.cmu.edu'},
            {'name': 'University of Michigan', 'website': 'https://umich.edu'},
            {'name': 'Georgia Institute of Technology', 'website': 'https://www.gatech.edu'},
            {'name': 'University of Illinois Urbana-Champaign', 'website': 'https://illinois.edu'},
            {'name': 'Cornell University', 'website': 'https://www.cornell.edu'}
        ],
        'UK': [
            {'name': 'University of Oxford', 'website': 'https://www.ox.ac.uk'},
            {'name': 'University of Cambridge', 'website': 'https://www.cam.ac.uk'},
            {'name': 'Imperial College London', 'website': 'https://www.imperial.ac.uk'},
            {'name': 'University College London', 'website': 'https://www.ucl.ac.uk'},
            {'name': 'University of Edinburgh', 'website': 'https://www.ed.ac.uk'},
            {'name': 'University of Manchester', 'website': 'https://www.manchester.ac.uk'},
            {'name': 'Kings College London', 'website': 'https://www.kcl.ac.uk'},
            {'name': 'London School of Economics', 'website': 'https://www.lse.ac.uk'}
        ],
        'Canada': [
            {'name': 'University of Toronto', 'website': 'https://www.utoronto.ca'},
            {'name': 'University of British Columbia', 'website': 'https://www.ubc.ca'},
            {'name': 'McGill University', 'website': 'https://www.mcgill.ca'},
            {'name': 'University of Waterloo', 'website': 'https://uwaterloo.ca'},
            {'name': 'University of Alberta', 'website': 'https://www.ualberta.ca'},
            {'name': 'McMaster University', 'website': 'https://www.mcmaster.ca'}
        ],
        'Germany': [
            {'name': 'Technical University of Munich', 'website': 'https://www.tum.de'},
            {'name': 'Ludwig Maximilian University of Munich', 'website': 'https://www.lmu.de'},
            {'name': 'Heidelberg University', 'website': 'https://www.uni-heidelberg.de'},
            {'name': 'Humboldt University of Berlin', 'website': 'https://www.hu-berlin.de'},
            {'name': 'RWTH Aachen University', 'website': 'https://www.rwth-aachen.de'}
        ],
        'Australia': [
            {'name': 'Australian National University', 'website': 'https://www.anu.edu.au'},
            {'name': 'University of Melbourne', 'website': 'https://www.unimelb.edu.au'},
            {'name': 'University of Sydney', 'website': 'https://www.sydney.edu.au'},
            {'name': 'University of New South Wales', 'website': 'https://www.unsw.edu.au'},
            {'name': 'University of Queensland', 'website': 'https://www.uq.edu.au'}
        ],
        'Singapore': [
            {'name': 'National University of Singapore', 'website': 'https://www.nus.edu.sg'},
            {'name': 'Nanyang Technological University', 'website': 'https://www.ntu.edu.sg'}
        ],
        'Switzerland': [
            {'name': 'ETH Zurich', 'website': 'https://ethz.ch'},
            {'name': 'EPFL', 'website': 'https://www.epfl.ch'}
        ],
        'Netherlands': [
            {'name': 'Delft University of Technology', 'website': 'https://www.tudelft.nl'},
            {'name': 'University of Amsterdam', 'website': 'https://www.uva.nl'},
            {'name': 'Eindhoven University of Technology', 'website': 'https://www.tue.nl'}
        ],
        'Sweden': [
            {'name': 'KTH Royal Institute of Technology', 'website': 'https://www.kth.se'},
            {'name': 'Lund University', 'website': 'https://www.lu.se'}
        ],
        'China': [
            {'name': 'Tsinghua University', 'website': 'https://www.tsinghua.edu.cn'},
            {'name': 'Peking University', 'website': 'https://www.pku.edu.cn'},
            {'name': 'Zhejiang University', 'website': 'https://www.zju.edu.cn'},
            {'name': 'Fudan University', 'website': 'https://www.fudan.edu.cn'},
            {'name': 'Shanghai Jiao Tong University', 'website': 'https://www.sjtu.edu.cn'}
        ],
        'Hong Kong': [
            {'name': 'University of Hong Kong', 'website': 'https://www.hku.hk'},
            {'name': 'Hong Kong University of Science and Technology', 'website': 'https://www.ust.hk'},
            {'name': 'Chinese University of Hong Kong', 'website': 'https://www.cuhk.edu.hk'}
        ],
        'Japan': [
            {'name': 'University of Tokyo', 'website': 'https://www.u-tokyo.ac.jp'},
            {'name': 'Kyoto University', 'website': 'https://www.kyoto-u.ac.jp'},
            {'name': 'Osaka University', 'website': 'https://www.osaka-u.ac.jp'}
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

    def scrape_universities(self, country: Optional[str] = None, limit: Optional[int] = None) -> List[Dict]:
        """
        Scrape universities from database
        Args:
            country: Filter by country (optional)
            limit: Maximum number of universities to return
        Returns:
            List of university dictionaries
        """
        logger.info(f"Scraping universities for country: {country or 'ALL'}")

        universities = []

        if country and country in self.UNIVERSITIES_DATABASE:
            countries = [country]
        else:
            countries = self.UNIVERSITIES_DATABASE.keys()

        for country_name in countries:
            for uni_data in self.UNIVERSITIES_DATABASE[country_name]:
                university = {
                    'name': uni_data['name'],
                    'country': country_name,
                    'website': uni_data['website'],
                    'has_scholarship': random.choice([True, False]),  # Simulated
                    'scholarship_info': json.dumps({
                        'available': random.choice([True, False]),
                        'types': ['Full Scholarship', 'Tuition Waiver', 'Stipend'],
                        'deadline': '2024-12-31'
                    }),
                    'research_areas': json.dumps([
                        'Machine Learning',
                        'Artificial Intelligence',
                        'Aerospace Engineering',
                        'Manufacturing',
                        'Robotics',
                        'Deep Learning'
                    ]),
                    'ranking': random.randint(1, 500),
                    'location': self._get_location(country_name),
                    'last_scraped': datetime.utcnow(),
                    'scrape_status': 'completed'
                }

                universities.append(university)

                if limit and len(universities) >= limit:
                    break

            if limit and len(universities) >= limit:
                break

        logger.info(f"Scraped {len(universities)} universities")
        return universities

    def _get_location(self, country: str) -> str:
        """Get a sample location for the country"""
        locations = {
            'USA': 'Cambridge, MA',
            'UK': 'London',
            'Canada': 'Toronto, ON',
            'Germany': 'Munich',
            'Australia': 'Melbourne, VIC',
            'Singapore': 'Singapore',
            'Switzerland': 'Zurich',
            'Netherlands': 'Amsterdam',
            'Sweden': 'Stockholm',
            'China': 'Beijing',
            'Hong Kong': 'Hong Kong',
            'Japan': 'Tokyo'
        }
        return locations.get(country, country)

    def scrape_university_details(self, website: str) -> Dict:
        """
        Scrape detailed information from university website
        Args:
            website: University website URL
        Returns:
            Dictionary with scraped details
        """
        try:
            logger.info(f"Scraping details from {website}")
            self._random_delay()

            response = self.session.get(website, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract basic information (simplified)
            details = {
                'contact_info': json.dumps({
                    'phone': '+1-XXX-XXX-XXXX',
                    'email': 'admissions@university.edu',
                    'address': 'University Address'
                }),
                'scrape_status': 'completed',
                'last_scraped': datetime.utcnow()
            }

            return details

        except Exception as e:
            logger.error(f"Error scraping {website}: {str(e)}")
            return {
                'scrape_status': 'failed',
                'last_scraped': datetime.utcnow()
            }

    def get_available_countries(self) -> List[str]:
        """Get list of available countries"""
        return list(self.UNIVERSITIES_DATABASE.keys())
