"""
Scraping CLI Commands
"""
import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from models import db, University, Professor
from services.scraper import UniversityScraper, ProfessorScraper


@click.group()
def scrape_group():
    """Web scraping commands"""
    pass


@scrape_group.command('universities')
@click.option('--country', '-c', help='Filter by country')
@click.option('--limit', '-l', default=50, help='Maximum universities to scrape')
def scrape_universities(country, limit):
    """Scrape universities"""
    try:
        click.echo(f'Scraping universities (country: {country or "ALL"}, limit: {limit})...')

        app = create_app()
        with app.app_context():
            scraper = UniversityScraper()
            universities_data = scraper.scrape_universities(country=country, limit=limit)

            saved_count = 0
            for uni_data in universities_data:
                existing = University.query.filter_by(
                    name=uni_data['name'],
                    country=uni_data['country']
                ).first()

                if existing:
                    for key, value in uni_data.items():
                        setattr(existing, key, value)
                else:
                    university = University(**uni_data)
                    db.session.add(university)

                saved_count += 1

            db.session.commit()

            click.echo(click.style(f'✓ Successfully scraped {saved_count} universities!', fg='green'))

    except Exception as e:
        click.echo(click.style(f'✗ Error scraping universities: {str(e)}', fg='red'))


@scrape_group.command('professors')
@click.option('--university', '-u', required=True, help='University name or ID')
@click.option('--limit', '-l', default=50, help='Maximum professors to scrape')
def scrape_professors(university, limit):
    """Scrape professors for a university"""
    try:
        click.echo(f'Scraping professors for {university} (limit: {limit})...')

        app = create_app()
        with app.app_context():
            # Find university
            if university.isdigit():
                uni = University.query.get(int(university))
            else:
                uni = University.query.filter(University.name.contains(university)).first()

            if not uni:
                click.echo(click.style(f'✗ University not found: {university}', fg='red'))
                return

            scraper = ProfessorScraper()
            professors_data = scraper.scrape_professors(
                university_id=uni.id,
                university_name=uni.name,
                limit=limit
            )

            saved_count = 0
            for prof_data in professors_data:
                existing = Professor.query.filter_by(
                    university_id=uni.id,
                    email=prof_data['email']
                ).first()

                if existing:
                    for key, value in prof_data.items():
                        setattr(existing, key, value)
                else:
                    professor = Professor(**prof_data)
                    db.session.add(professor)

                saved_count += 1

            db.session.commit()

            click.echo(click.style(f'✓ Successfully scraped {saved_count} professors!', fg='green'))

    except Exception as e:
        click.echo(click.style(f'✗ Error scraping professors: {str(e)}', fg='red'))


# Export as 'scrape' command
scrape = scrape_group
