"""
Authentication Routes
User registration, login, and authentication
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from datetime import timedelta

from models import db, User
from services.utils.validators import (
    validate_email,
    validate_password,
    validate_required_fields
)


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        # Validate required fields
        is_valid, error = validate_required_fields(data, ['email', 'password', 'name'])
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        email = data['email'].lower().strip()
        password = data['password']
        name = data['name'].strip()

        # Validate email format
        if not validate_email(email):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400

        # Validate password strength
        is_valid, error = validate_password(password)
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 409

        # Create new user
        user = User(
            email=email,
            password=password,
            name=name,
            research_interests=data.get('research_interests', []),
            target_countries=data.get('target_countries', []),
            phone=data.get('phone'),
            country=data.get('country')
        )

        db.session.add(user)
        db.session.commit()

        current_app.logger.info(f'New user registered: {email}')

        # Create access tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Registration error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Registration failed',
            'message': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens"""
    try:
        data = request.get_json()

        # Validate required fields
        is_valid, error = validate_required_fields(data, ['email', 'password'])
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        email = data['email'].lower().strip()
        password = data['password']

        # Find user
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401

        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is disabled'
            }), 403

        # Update last login
        user.update_last_login()

        # Create access tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        current_app.logger.info(f'User logged in: {email}')

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    except Exception as e:
        current_app.logger.error(f'Login error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Login failed',
            'message': str(e)
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token"""
    try:
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)

        return jsonify({
            'success': True,
            'access_token': access_token
        }), 200

    except Exception as e:
        current_app.logger.error(f'Token refresh error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Token refresh failed'
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get current user error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to get user information'
        }), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate required fields
        is_valid, error = validate_required_fields(data, ['current_password', 'new_password'])
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        # Verify current password
        if not user.check_password(data['current_password']):
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect'
            }), 401

        # Validate new password
        is_valid, error = validate_password(data['new_password'])
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        # Update password
        user.set_password(data['new_password'])
        db.session.commit()

        current_app.logger.info(f'Password changed for user: {user.email}')

        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Change password error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Password change failed'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client should delete tokens)"""
    try:
        user_id = get_jwt_identity()
        current_app.logger.info(f'User logged out: {user_id}')

        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Logout failed'
        }), 500
