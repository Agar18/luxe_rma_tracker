from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.auth_utils import generate_token


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = generate_password_hash(data['password'])

    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=hashed_pw,
        role='customer'
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully.'}), 201

from app.utils.auth_utils import generate_token

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password_hash, data['password']):
        token = generate_token(user.id, user.role)
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'token': token,
            'role': user.role  # NEW: include role
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401


