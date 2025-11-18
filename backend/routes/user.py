"""
User Profile Routes
User profile and settings management
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import db, User
from services.utils.validators import validate_email, validate_required_fields


user_bp = Blueprint('user', __name__)


@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
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
        current_app.logger.error(f'Get profile error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve profile',
            'message': str(e)
        }), 500


@user_bp.route('/', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user's profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        data = request.get_json()

        # Update basic fields
        if 'name' in data:
            user.name = data['name'].strip()

        if 'phone' in data:
            user.phone = data['phone']

        if 'country' in data:
            user.country = data['country']

        # Update email with validation
        if 'email' in data:
            new_email = data['email'].lower().strip()
            if new_email != user.email:
                # Validate email format
                if not validate_email(new_email):
                    return jsonify({
                        'success': False,
                        'error': 'Invalid email format'
                    }), 400

                # Check if email already exists
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user:
                    return jsonify({
                        'success': False,
                        'error': 'Email already in use'
                    }), 409

                user.email = new_email

        # Update research profile
        if 'research_interests' in data:
            user.research_interests = data['research_interests']

        if 'target_countries' in data:
            user.target_countries = data['target_countries']

        if 'preferences' in data:
            user.preferences = data['preferences']

        # Update CV information
        if 'cv_filename' in data:
            user.cv_filename = data['cv_filename']

        if 'cv_path' in data:
            user.cv_path = data['cv_path']

        user.updated_at = datetime.utcnow()
        db.session.commit()

        current_app.logger.info(f'Profile updated for user: {user.email}')

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update profile error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update profile',
            'message': str(e)
        }), 500


@user_bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_account():
    """Delete current user's account"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        user_email = user.email
        db.session.delete(user)
        db.session.commit()

        current_app.logger.info(f'User account deleted: {user_email}')

        return jsonify({
            'success': True,
            'message': 'Account deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Delete account error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to delete account',
            'message': str(e)
        }), 500


@user_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    """Get user preferences"""
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
            'preferences': user.preferences or {}
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get preferences error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve preferences',
            'message': str(e)
        }), 500


@user_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    """Update user preferences"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        data = request.get_json()

        # Merge new preferences with existing ones
        current_preferences = user.preferences or {}
        current_preferences.update(data)
        user.preferences = current_preferences

        user.updated_at = datetime.utcnow()
        db.session.commit()

        current_app.logger.info(f'Preferences updated for user: {user.email}')

        return jsonify({
            'success': True,
            'message': 'Preferences updated successfully',
            'preferences': user.preferences
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update preferences error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update preferences',
            'message': str(e)
        }), 500


@user_bp.route('/research-profile', methods=['GET'])
@jwt_required()
def get_research_profile():
    """Get user's research profile"""
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
            'research_profile': {
                'research_interests': user.research_interests or [],
                'target_countries': user.target_countries or [],
                'has_cv': bool(user.cv_path),
                'cv_filename': user.cv_filename
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get research profile error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve research profile',
            'message': str(e)
        }), 500


@user_bp.route('/research-profile', methods=['PUT'])
@jwt_required()
def update_research_profile():
    """Update user's research profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        data = request.get_json()

        if 'research_interests' in data:
            user.research_interests = data['research_interests']

        if 'target_countries' in data:
            user.target_countries = data['target_countries']

        user.updated_at = datetime.utcnow()
        db.session.commit()

        current_app.logger.info(f'Research profile updated for user: {user.email}')

        return jsonify({
            'success': True,
            'message': 'Research profile updated successfully',
            'research_profile': {
                'research_interests': user.research_interests or [],
                'target_countries': user.target_countries or []
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update research profile error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update research profile',
            'message': str(e)
        }), 500


@user_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_user_statistics():
    """Get user's overall statistics"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        # Get counts from relationships
        applications_count = user.applications.count() if hasattr(user, 'applications') else 0
        batches_count = user.email_batches.count() if hasattr(user, 'email_batches') else 0

        # Calculate days since registration
        days_since_registration = (datetime.utcnow() - user.created_at).days if user.created_at else 0

        return jsonify({
            'success': True,
            'statistics': {
                'applications_count': applications_count,
                'email_batches_count': batches_count,
                'days_since_registration': days_since_registration,
                'account_created': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'is_verified': user.is_verified,
                'has_cv': bool(user.cv_path)
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get user statistics error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve user statistics',
            'message': str(e)
        }), 500
