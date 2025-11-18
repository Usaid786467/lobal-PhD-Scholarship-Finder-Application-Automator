"""
University Tests
Tests for university discovery and search
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, University
from services.scraper import UniversityScraper


@pytest.fixture
def app():
    """Create test app"""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def auth_token(client):
    """Create authenticated user and return token"""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })
    return response.get_json()['access_token']


def test_university_scraper():
    """Test university scraper"""
    scraper = UniversityScraper()
    universities = scraper.scrape_universities(country='USA', limit=5)

    assert len(universities) > 0
    assert universities[0]['name']
    assert universities[0]['country'] == 'USA'


def test_discover_universities(client, auth_token):
    """Test university discovery endpoint"""
    response = client.post('/api/universities/discover',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'country': 'USA', 'limit': 5}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['count'] > 0


def test_search_universities(client, auth_token, app):
    """Test university search"""
    # Add test university
    with app.app_context():
        uni = University(
            name='Test University',
            country='USA',
            website='https://test.edu',
            has_scholarship=True,
            research_areas='["Machine Learning"]'
        )
        db.session.add(uni)
        db.session.commit()

    # Search
    response = client.get('/api/universities/search?country=USA',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert 'universities' in data


def test_get_countries(client, auth_token):
    """Test getting available countries"""
    response = client.get('/api/universities/countries',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert 'countries' in data
    assert len(data['countries']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
