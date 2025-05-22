from flask import Blueprint, request, jsonify
from app import db
from app.models.rma import RMA
from datetime import datetime
import uuid
from app.models.marker import Marker
from app.models.user import User

rma_bp = Blueprint('rma', __name__)

@rma_bp.route('/create', methods=['POST'])
def create_rma():
    data = request.json
    rma_number = f'RMA-{uuid.uuid4().hex[:8].upper()}'

    rma = RMA(
        marker_id=data['marker_id'],
        user_id=data['user_id'],
        rma_number=rma_number,
        created_at=datetime.utcnow(),
        status='open'
    )
    db.session.add(rma)
    db.session.commit()

    return jsonify({'message': 'RMA created', 'rma_number': rma_number}), 201

@rma_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_rmas(user_id):
    from app.models.rma import RMA

    rmas = RMA.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'rma_number': r.rma_number,
            'status': r.status
        } for r in rmas
    ])

@rma_bp.route('/all', methods=['GET'])
def get_all_rmas():
    rmas = db.session.query(RMA, Marker, User)\
        .join(Marker, RMA.marker_id == Marker.id)\
        .join(User, RMA.user_id == User.id)\
        .all()

    return jsonify([
        {
            'rma_number': rma.rma_number,
            'status': rma.status,
            'serial_number': marker.serial_number,
            'model': marker.model,
            'owner_name': user.name,
            'owner_email': user.email
        }
        for rma, marker, user in rmas
    ])

