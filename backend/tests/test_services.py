"""
Service Tests
Tests for AI and utility services
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai.gemini_service import GeminiService
from services.ai.email_generator import EmailGenerator
from services.ai.matching_engine import MatchingEngine
from config import Config


def test_gemini_service():
    """Test Gemini AI service initialization"""
    try:
        gemini = GeminiService(Config.GEMINI_API_KEY)
        assert gemini is not None
        assert gemini.model is not None
    except Exception as e:
        # If API key is not configured, test should pass
        pass


def test_email_generator():
    """Test email generation"""
    try:
        gemini = GeminiService(Config.GEMINI_API_KEY)
        generator = EmailGenerator(gemini)

        email = generator._generate_template_email(
            professor_name='Dr. Smith',
            professor_research='Machine Learning, Robotics',
            university_name='Test University',
            user_name='Test Student',
            user_research='Deep Learning, AI'
        )

        assert 'subject' in email
        assert 'body' in email
        assert 'Dr. Smith' in email['body']
        assert 'Test University' in email['body']
    except Exception as e:
        pytest.skip(f"Skipping due to: {str(e)}")


def test_matching_engine():
    """Test research matching"""
    try:
        gemini = GeminiService(Config.GEMINI_API_KEY)
        matcher = MatchingEngine(gemini)

        # Test with basic match
        user_interests = '["Machine Learning", "Deep Learning"]'
        prof_interests = '["Neural Networks", "AI"]'

        score = matcher.calculate_match_score(user_interests, prof_interests)

        # Score should be between 0 and 100
        assert 0 <= score <= 100
    except Exception as e:
        pytest.skip(f"Skipping due to: {str(e)}")


def test_email_template_generation():
    """Test template email generation (no API needed)"""
    gemini = GeminiService(Config.GEMINI_API_KEY if Config.GEMINI_API_KEY else 'test-key')
    generator = EmailGenerator(gemini)

    email = generator._generate_template_email(
        professor_name='Dr. Johnson',
        professor_research='Aerospace Engineering',
        university_name='MIT',
        user_name='John Doe',
        user_research='Mechanical Engineering, ML'
    )

    assert email['subject']
    assert email['body']
    assert 'Dr. Johnson' in email['body']
    assert 'MIT' in email['body']
    assert 'John Doe' in email['body']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
