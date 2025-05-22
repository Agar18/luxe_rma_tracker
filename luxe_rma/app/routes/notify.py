from flask import Blueprint, request, jsonify
from app.services.email_service import send_email

notify_bp = Blueprint('notify', __name__)

@notify_bp.route('/customer', methods=['POST'])
def notify_customer():
    data = request.json

    send_email(
        to=data['email'],
        subject=data['subject'],
        body=data['message']
    )
    return jsonify({'message': 'Email sent successfully'})
