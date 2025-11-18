"""
Helper Utilities
General helper functions
"""

import os
import re
import uuid
import hashlib
from datetime import datetime
from dateutil import parser as date_parser
from typing import Optional


def generate_tracking_id() -> str:
    """Generate a unique tracking ID"""
    return str(uuid.uuid4())


def generate_short_id(length: int = 8) -> str:
    """Generate a short unique ID"""
    return str(uuid.uuid4())[:length]


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be filesystem-safe"""
    # Remove invalid characters
    sanitized = re.sub(r'[^\w\s\-\.]', '', filename)

    # Replace spaces with underscores
    sanitized = re.sub(r'\s+', '_', sanitized)

    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')

    return sanitized or 'unnamed_file'


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''


def parse_date(date_string: str) -> Optional[datetime]:
    """Parse date string to datetime object"""
    if not date_string:
        return None

    try:
        return date_parser.parse(date_string)
    except (ValueError, TypeError):
        return None


def format_date(date_obj: datetime, format_str: str = '%Y-%m-%d') -> str:
    """Format datetime object to string"""
    if not date_obj:
        return ''
    return date_obj.strftime(format_str)


def calculate_md5(content: str) -> str:
    """Calculate MD5 hash of content"""
    return hashlib.md5(content.encode()).hexdigest()


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to maximum length"""
    if not text or len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL"""
    if not url:
        return None

    # Remove protocol
    domain = re.sub(r'^https?://', '', url)

    # Remove path
    domain = domain.split('/')[0]

    # Remove www
    domain = re.sub(r'^www\.', '', domain)

    return domain.lower()


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    # Convert to lowercase
    slug = text.lower()

    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)

    # Remove leading/trailing hyphens
    slug = slug.strip('-')

    return slug


def chunk_list(lst: list, chunk_size: int):
    """Split list into chunks of specified size"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def safe_int(value, default: int = 0) -> int:
    """Safely convert value to int"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default: float = 0.0) -> float:
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def percentage(part: float, whole: float, decimals: int = 2) -> float:
    """Calculate percentage"""
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, decimals)


def ensure_directory_exists(directory: str):
    """Ensure directory exists, create if it doesn't"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def file_size_human_readable(size_bytes: int) -> str:
    """Convert file size in bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"
