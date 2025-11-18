"""
Authentication Routes
Handles user registration, login, and profile management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from email_validator import validate_email, EmailNotValidError
import json

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    POST /api/auth/register
    Body: {email, password, name, research_interests}
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'error': 'Email, password, and name are required'}), 400

        # Validate email format
        try:
            email_info = validate_email(data['email'])
            email = email_info.normalized
        except EmailNotValidError as e:
            return jsonify({'error': str(e)}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400

        # Create new user
        user = User(
            email=email,
            name=data['name'],
            research_interests=json.dumps(data.get('research_interests', []))
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        # Generate access token
        access_token = create_access_token(identity=user.id)

        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    POST /api/auth/login
    Body: {email, password}
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400

        # Find user
        user = User.query.filter_by(email=data['email']).first()

        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Generate access token
        access_token = create_access_token(identity=user.id)

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get user profile
    GET /api/auth/profile
    Headers: Authorization: Bearer <token>
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update user profile
    PUT /api/auth/profile
    Headers: Authorization: Bearer <token>
    Body: {name, research_interests, cv_path}
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()

        # Update fields
        if 'name' in data:
            user.name = data['name']
        if 'research_interests' in data:
            user.research_interests = json.dumps(data['research_interests'])
        if 'cv_path' in data:
            user.cv_path = data['cv_path']

        db.session.commit()

        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
