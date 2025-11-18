"""
General helper utilities
"""
import hashlib
import secrets
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import json


def generate_random_string(length: int = 32, include_special_chars: bool = False) -> str:
    """
    Generate a random string

    Args:
        length: Length of string
        include_special_chars: Include special characters

    Returns:
        Random string
    """
    characters = string.ascii_letters + string.digits

    if include_special_chars:
        characters += string.punctuation

    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_token(length: int = 32) -> str:
    """
    Generate a secure token

    Args:
        length: Token length

    Returns:
        Secure token
    """
    return secrets.token_urlsafe(length)


def hash_string(text: str) -> str:
    """
    Hash a string using SHA-256

    Args:
        text: Text to hash

    Returns:
        Hashed string
    """
    return hashlib.sha256(text.encode()).hexdigest()


def calculate_percentage(part: float, total: float, decimal_places: int = 2) -> float:
    """
    Calculate percentage

    Args:
        part: Part value
        total: Total value
        decimal_places: Number of decimal places

    Returns:
        Percentage value
    """
    if total == 0:
        return 0.0

    percentage = (part / total) * 100
    return round(percentage, decimal_places)


def format_date(date: datetime, format: str = '%Y-%m-%d') -> str:
    """
    Format datetime object to string

    Args:
        date: Datetime object
        format: Date format string

    Returns:
        Formatted date string
    """
    if not date:
        return ''

    return date.strftime(format)


def parse_date(date_string: str, format: str = '%Y-%m-%d') -> Optional[datetime]:
    """
    Parse date string to datetime object

    Args:
        date_string: Date string
        format: Date format string

    Returns:
        Datetime object or None
    """
    try:
        return datetime.strptime(date_string, format)
    except (ValueError, TypeError):
        return None


def get_days_difference(date1: datetime, date2: datetime) -> int:
    """
    Get difference in days between two dates

    Args:
        date1: First date
        date2: Second date

    Returns:
        Number of days
    """
    delta = date2 - date1
    return abs(delta.days)


def is_date_in_past(date: datetime) -> bool:
    """
    Check if date is in the past

    Args:
        date: Date to check

    Returns:
        True if in past, False otherwise
    """
    return date < datetime.utcnow()


def add_days_to_date(date: datetime, days: int) -> datetime:
    """
    Add days to date

    Args:
        date: Starting date
        days: Number of days to add

    Returns:
        New datetime
    """
    return date + timedelta(days=days)


def truncate_string(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate string to maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated string
    """
    if not text or len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def safe_json_loads(json_string: str, default: Any = None) -> Any:
    """
    Safely load JSON string

    Args:
        json_string: JSON string
        default: Default value if parsing fails

    Returns:
        Parsed JSON or default value
    """
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(data: Any, default: str = '{}') -> str:
    """
    Safely dump data to JSON string

    Args:
        data: Data to dump
        default: Default value if dumping fails

    Returns:
        JSON string or default value
    """
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        return default


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks

    Args:
        lst: List to split
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """
    Flatten nested list

    Args:
        nested_list: Nested list

    Returns:
        Flattened list
    """
    return [item for sublist in nested_list for item in sublist]


def remove_duplicates(lst: List[Any]) -> List[Any]:
    """
    Remove duplicates from list while preserving order

    Args:
        lst: List with duplicates

    Returns:
        List without duplicates
    """
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def dict_to_query_string(params: Dict[str, Any]) -> str:
    """
    Convert dictionary to query string

    Args:
        params: Parameters dictionary

    Returns:
        Query string
    """
    if not params:
        return ''

    query_parts = []
    for key, value in params.items():
        if value is not None:
            query_parts.append(f"{key}={value}")

    return '&'.join(query_parts)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers

    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero

    Returns:
        Result or default value
    """
    if denominator == 0:
        return default

    return numerator / denominator


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human-readable format

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

    return f"{size_bytes:.2f} PB"


def extract_domain_from_url(url: str) -> Optional[str]:
    """
    Extract domain from URL

    Args:
        url: URL string

    Returns:
        Domain or None
    """
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return None


def is_valid_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Check if file has valid extension

    Args:
        filename: Filename to check
        allowed_extensions: List of allowed extensions (e.g., ['pdf', 'doc'])

    Returns:
        True if valid, False otherwise
    """
    if not filename or '.' not in filename:
        return False

    extension = filename.rsplit('.', 1)[1].lower()
    return extension in [ext.lower() for ext in allowed_extensions]
