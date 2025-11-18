"""
Authentication routes for user registration and login
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import datetime
from models import db, User
import re

# Create blueprint
auth_bp = Blueprint('auth', __name__)


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength
    - At least 8 characters
    - Contains uppercase and lowercase letters
    - Contains numbers
    - Contains special characters
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, "Password is valid"


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    POST /api/auth/register
    {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "name": "John Doe",
        "research_interests": ["Deep Learning", "Manufacturing"],
        "target_countries": ["USA", "Canada", "UK"]
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        email = data['email'].lower().strip()
        password = data['password']
        name = data['name'].strip()

        # Validate email
        if not validate_email(email):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 409

        # Validate password
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': message
            }), 400

        # Create new user
        user = User(
            email=email,
            password=password,  # Will be hashed in User.__init__
            name=name,
            research_interests=data.get('research_interests'),
            target_countries=data.get('target_countries')
        )

        db.session.add(user)
        db.session.commit()

        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Registration failed',
            'message': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    ---
    POST /api/auth/login
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400

        email = data['email'].lower().strip()
        password = data['password']

        # Find user
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401

        # Check password
        if not user.check_password(password):
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401

        # Check if user is active
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is deactivated'
            }), 403

        # Update last login
        user.update_last_login()

        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Login failed',
            'message': str(e)
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    ---
    POST /api/auth/refresh
    Headers: Authorization: Bearer <refresh_token>
    """
    try:
        current_user_id = get_jwt_identity()

        # Create new access token
        new_access_token = create_access_token(identity=current_user_id)

        return jsonify({
            'success': True,
            'message': 'Token refreshed successfully',
            'data': {
                'access_token': new_access_token
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Token refresh failed',
            'message': str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user (client should discard tokens)
    ---
    POST /api/auth/logout
    Headers: Authorization: Bearer <access_token>
    """
    try:
        # In a production app, you might want to blacklist the token
        # For now, we just return success and let client handle token removal

        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Logout failed',
            'message': str(e)
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user information
    ---
    GET /api/auth/me
    Headers: Authorization: Bearer <access_token>
    """
    try:
        current_user_id = get_jwt_identity()

        user = User.query.get(current_user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict()
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get user information',
            'message': str(e)
        }), 500


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Request password reset (placeholder for now)
    ---
    POST /api/auth/forgot-password
    {
        "email": "user@example.com"
    }
    """
    try:
        data = request.get_json()

        if 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400

        email = data['email'].lower().strip()

        # Check if user exists
        user = User.query.filter_by(email=email).first()

        # Always return success for security (don't reveal if email exists)
        return jsonify({
            'success': True,
            'message': 'If the email exists, a password reset link will be sent'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Password reset request failed',
            'message': str(e)
        }), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password with token (placeholder for now)
    ---
    POST /api/auth/reset-password
    {
        "token": "reset_token",
        "new_password": "NewSecurePass123!"
    }
    """
    try:
        data = request.get_json()

        required_fields = ['token', 'new_password']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        # TODO: Implement token validation and password reset
        # For now, return success placeholder

        return jsonify({
            'success': True,
            'message': 'Password reset successful (not implemented yet)'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Password reset failed',
            'message': str(e)
        }), 500
