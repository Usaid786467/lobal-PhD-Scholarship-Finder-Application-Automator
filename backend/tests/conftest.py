"""
Pytest Configuration
Shared fixtures and configuration for all tests
"""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
