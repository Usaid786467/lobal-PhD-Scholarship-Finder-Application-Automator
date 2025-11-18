"""
Input validation utilities
"""
import re
from datetime import datetime
from typing import List, Dict, Any, Optional


def validate_email(email: str) -> bool:
    """
    Validate email format

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_url(url: str) -> bool:
    """
    Validate URL format

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    if not url:
        return False

    pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    return re.match(pattern, url) is not None


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> tuple:
    """
    Validate that all required fields are present in data

    Args:
        data: Data dictionary
        required_fields: List of required field names

    Returns:
        Tuple of (is_valid, missing_fields)
    """
    missing_fields = []

    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            missing_fields.append(field)

    is_valid = len(missing_fields) == 0
    return is_valid, missing_fields


def validate_date_string(date_string: str, format: str = '%Y-%m-%d') -> bool:
    """
    Validate date string format

    Args:
        date_string: Date string to validate
        format: Expected date format

    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_string, format)
        return True
    except (ValueError, TypeError):
        return False


def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize string input

    Args:
        text: Text to sanitize
        max_length: Maximum length (optional)

    Returns:
        Sanitized text
    """
    if not text:
        return ''

    # Remove leading/trailing whitespace
    text = text.strip()

    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')

    # Truncate if max_length specified
    if max_length and len(text) > max_length:
        text = text[:max_length]

    return text


def validate_pagination_params(page: int, per_page: int, max_per_page: int = 100) -> tuple:
    """
    Validate pagination parameters

    Args:
        page: Page number
        per_page: Items per page
        max_per_page: Maximum items per page

    Returns:
        Tuple of (is_valid, error_message)
    """
    if page < 1:
        return False, "Page must be >= 1"

    if per_page < 1:
        return False, "Per page must be >= 1"

    if per_page > max_per_page:
        return False, f"Per page must be <= {max_per_page}"

    return True, None


def validate_country_code(country_code: str) -> bool:
    """
    Validate country code (basic validation)

    Args:
        country_code: Country code to validate

    Returns:
        True if valid, False otherwise
    """
    if not country_code:
        return False

    # Should be 2-3 characters, alphanumeric
    return len(country_code) in [2, 3] and country_code.isalpha()


def validate_enum_value(value: str, valid_values: List[str]) -> tuple:
    """
    Validate enum value

    Args:
        value: Value to validate
        valid_values: List of valid values

    Returns:
        Tuple of (is_valid, error_message)
    """
    if value not in valid_values:
        return False, f"Invalid value. Must be one of: {', '.join(valid_values)}"

    return True, None


def validate_positive_integer(value: Any) -> tuple:
    """
    Validate positive integer

    Args:
        value: Value to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        int_value = int(value)
        if int_value <= 0:
            return False, "Value must be a positive integer"
        return True, None
    except (ValueError, TypeError):
        return False, "Value must be an integer"


def validate_range(value: Any, min_val: float, max_val: float) -> tuple:
    """
    Validate value is within range

    Args:
        value: Value to validate
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        num_value = float(value)
        if num_value < min_val or num_value > max_val:
            return False, f"Value must be between {min_val} and {max_val}"
        return True, None
    except (ValueError, TypeError):
        return False, "Value must be a number"
