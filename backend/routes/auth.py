"""
Authentication Routes for PhD Application Automator
Handles user registration, login, and authentication
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from models import get_session, User
from datetime import datetime, timedelta
import re

auth_bp = Blueprint('auth', __name__)


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength
    Requirements: At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    return True, "Password is valid"


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user

    Request JSON:
        email: string (required)
        password: string (required)
        name: string (required)
        research_interests: list of strings (optional)
        target_countries: list of strings (optional)

    Returns:
        201: User created successfully
        400: Invalid input
        409: Email already exists
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data or not all(k in data for k in ['email', 'password', 'name']):
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Email, password, and name are required'
            }), 400

        email = data['email'].strip().lower()
        password = data['password']
        name = data['name'].strip()

        # Validate email
        if not validate_email(email):
            return jsonify({
                'error': 'Invalid email',
                'message': 'Please provide a valid email address'
            }), 400

        # Validate password
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({
                'error': 'Weak password',
                'message': message
            }), 400

        # Check if user already exists
        session = get_session()
        existing_user = session.query(User).filter_by(email=email).first()

        if existing_user:
            return jsonify({
                'error': 'Email already registered',
                'message': 'An account with this email already exists'
            }), 409

        # Create new user
        user = User(
            email=email,
            password=password,
            name=name,
            research_interests=data.get('research_interests', []),
            target_countries=data.get('target_countries', []),
            education_background=data.get('education_background'),
            target_degree=data.get('target_degree')
        )

        session.add(user)
        session.commit()

        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        current_app.logger.info(f'New user registered: {email}')

        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201

    except Exception as e:
        current_app.logger.error(f'Registration error: {str(e)}')
        return jsonify({
            'error': 'Registration failed',
            'message': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user

    Request JSON:
        email: string (required)
        password: string (required)

    Returns:
        200: Login successful
        400: Invalid input
        401: Invalid credentials
    """
    try:
        data = request.get_json()

        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({
                'error': 'Missing credentials',
                'message': 'Email and password are required'
            }), 400

        email = data['email'].strip().lower()
        password = data['password']

        # Find user
        session = get_session()
        user = session.query(User).filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Email or password is incorrect'
            }), 401

        if not user.is_active:
            return jsonify({
                'error': 'Account inactive',
                'message': 'Your account has been deactivated'
            }), 401

        # Update last login
        user.update_last_login()
        session.commit()

        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        current_app.logger.info(f'User logged in: {email}')

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    except Exception as e:
        current_app.logger.error(f'Login error: {str(e)}')
        return jsonify({
            'error': 'Login failed',
            'message': str(e)
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token

    Returns:
        200: New access token
        401: Invalid refresh token
    """
    try:
        user_id = get_jwt_identity()

        # Verify user still exists and is active
        session = get_session()
        user = session.query(User).filter_by(id=user_id).first()

        if not user or not user.is_active:
            return jsonify({
                'error': 'Invalid token',
                'message': 'User not found or inactive'
            }), 401

        # Create new access token
        access_token = create_access_token(identity=user_id)

        return jsonify({
            'access_token': access_token
        }), 200

    except Exception as e:
        current_app.logger.error(f'Token refresh error: {str(e)}')
        return jsonify({
            'error': 'Token refresh failed',
            'message': str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user (client-side token removal)

    Returns:
        200: Logout successful
    """
    # Note: With JWT, actual logout happens client-side by removing the token
    # This endpoint is mainly for logging purposes
    user_id = get_jwt_identity()
    current_app.logger.info(f'User logged out: {user_id}')

    return jsonify({
        'message': 'Logout successful'
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user

    Returns:
        200: User data
        401: Not authenticated
        404: User not found
    """
    try:
        user_id = get_jwt_identity()

        session = get_session()
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'User account not found'
            }), 404

        return jsonify({
            'user': user.to_dict()
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get current user error: {str(e)}')
        return jsonify({
            'error': 'Failed to get user',
            'message': str(e)
        }), 500


@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """
    Verify user email (placeholder for email verification)

    Request JSON:
        token: string (required)

    Returns:
        200: Email verified
        400: Invalid token
    """
    # TODO: Implement email verification logic
    return jsonify({
        'message': 'Email verification not yet implemented'
    }), 501


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Request password reset (placeholder)

    Request JSON:
        email: string (required)

    Returns:
        200: Reset email sent
        404: User not found
    """
    try:
        data = request.get_json()

        if not data or 'email' not in data:
            return jsonify({
                'error': 'Missing email',
                'message': 'Email is required'
            }), 400

        email = data['email'].strip().lower()

        session = get_session()
        user = session.query(User).filter_by(email=email).first()

        # Always return success to prevent email enumeration
        # TODO: Implement actual password reset email
        current_app.logger.info(f'Password reset requested for: {email}')

        return jsonify({
            'message': 'If an account exists with this email, a password reset link has been sent'
        }), 200

    except Exception as e:
        current_app.logger.error(f'Forgot password error: {str(e)}')
        return jsonify({
            'error': 'Request failed',
            'message': str(e)
        }), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password (placeholder)

    Request JSON:
        token: string (required)
        new_password: string (required)

    Returns:
        200: Password reset successful
        400: Invalid token or weak password
    """
    # TODO: Implement password reset logic
    return jsonify({
        'message': 'Password reset not yet implemented'
    }), 501
