"""
User Profile Routes for PhD Application Automator
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_session, User
from werkzeug.utils import secure_filename
import os

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        session = get_session()
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'user': user.to_dict(include_sensitive=True)}), 200

    except Exception as e:
        current_app.logger.error(f'Get profile error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        session = get_session()
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Update allowed fields
        allowed_fields = ['name', 'research_interests', 'target_countries',
                         'education_background', 'target_degree']

        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        session.commit()
        current_app.logger.info(f'Profile updated for user {user_id}')

        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        current_app.logger.error(f'Update profile error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@user_bp.route('/cv-upload', methods=['POST'])
@jwt_required()
def upload_cv():
    """Upload CV file"""
    try:
        user_id = get_jwt_identity()

        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Validate file extension
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
        if not any(file.filename.lower().endswith(f'.{ext}') for ext in allowed_extensions):
            return jsonify({
                'error': 'Invalid file type',
                'message': f'Allowed types: {", ".join(allowed_extensions)}'
            }), 400

        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'cv_{user_id}_{timestamp}_{filename}'
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        file.save(file_path)

        # Update user record
        session = get_session()
        user = session.query(User).filter_by(id=user_id).first()
        user.cv_path = file_path
        user.cv_filename = file.filename
        user.cv_uploaded_at = datetime.utcnow()
        session.commit()

        current_app.logger.info(f'CV uploaded for user {user_id}')

        return jsonify({
            'message': 'CV uploaded successfully',
            'filename': file.filename
        }), 200

    except Exception as e:
        current_app.logger.error(f'CV upload error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@user_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    """Get user preferences"""
    try:
        user_id = get_jwt_identity()
        session = get_session()
        user = session.query(User).filter_by(id=user_id).first()

        return jsonify({'preferences': user.preferences or {}}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    """Update user preferences"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        session = get_session()
        user = session.query(User).filter_by(id=user_id).first()

        user.preferences = {**(user.preferences or {}), **data}
        session.commit()

        return jsonify({
            'message': 'Preferences updated',
            'preferences': user.preferences
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


from datetime import datetime
