#Can be changed
import jwt
from flask import request, jsonify
from functools import wraps
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'message': 'Missing or invalid token'}), 401

            token = auth_header.split(' ')[1]
            decoded = decode_token(token)

            if not decoded:
                return jsonify({'message': 'Token is invalid or expired'}), 401

            if role and decoded.get('role') != role:
                return jsonify({'message': 'Unauthorized'}), 403

            request.user = decoded  # attach user data to request context
            return f(*args, **kwargs)
        return wrapper
    return decorator
