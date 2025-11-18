"""
Validation Utilities
Input validation functions
"""

import re
import validators as v
from typing import Optional


def validate_email(email: str) -> bool:
    """Validate email address format"""
    if not email:
        return False
    return v.email(email.strip())


def validate_url(url: str) -> bool:
    """Validate URL format"""
    if not url:
        return False
    return v.url(url.strip())


def validate_phone(phone: str) -> bool:
    """Validate phone number format (basic validation)"""
    if not phone:
        return False

    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)\+\.]', '', phone)

    # Check if it's a valid number (10-15 digits)
    if re.match(r'^\d{10,15}$', cleaned):
        return True

    return False


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength
    Returns (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    return True, None


def validate_required_fields(data: dict, required_fields: list) -> tuple[bool, Optional[str]]:
    """
    Validate that all required fields are present
    Returns (is_valid, error_message)
    """
    missing_fields = []

    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)

    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"

    return True, None


def sanitize_string(text: str, max_length: int = None) -> str:
    """Sanitize string input"""
    if not text:
        return ""

    # Strip whitespace
    sanitized = text.strip()

    # Remove null bytes
    sanitized = sanitized.replace('\x00', '')

    # Limit length if specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """Validate file extension"""
    if not filename or '.' not in filename:
        return False

    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions
