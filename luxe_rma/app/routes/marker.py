from flask import Blueprint, request, jsonify
from app import db
from app.models.marker import Marker
from app.models.ownership import Ownership
from datetime import datetime
from app.utils.auth_utils import login_required

marker_bp = Blueprint('marker', __name__)

@marker_bp.route('/register-marker', methods=['POST'])
@login_required()
def register_marker():
    user = request.user
    if user.get('role') not in ['admin', 'tech']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.json

    marker = Marker(
        serial_number=data['serial_number'],
        model=data['model'],
        color=data['color'],
        date_made=datetime.strptime(data['date_made'], '%Y-%m-%d')
    )
    db.session.add(marker)
    db.session.flush()  # to get marker.id before commit

    ownership = Ownership(
        marker_id=marker.id,
        user_id=data['user_id'],
        ownership_start=datetime.utcnow(),
        purchased_from=data['purchased_from'],
        purchase_date=datetime.strptime(data['purchase_date'], '%Y-%m-%d')
    )
    db.session.add(ownership)
    db.session.commit()

    return jsonify({'message': 'Marker registered successfully.'}), 201

@marker_bp.route('/search/<serial>', methods=['GET'])
def search_marker(serial):
    marker = Marker.query.filter_by(serial_number=serial).first()
    if marker:
        return jsonify({
            'serial_number': marker.serial_number,
            'model': marker.model,
            'color': marker.color,
            'date_made': str(marker.date_made),
            'status': marker.status
        })
    return jsonify({'message': 'Marker not found'}), 404

@marker_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_markers(user_id):
    from app.models.marker import Marker
    from app.models.ownership import Ownership

    markers = db.session.query(Marker).join(Ownership).filter(Ownership.user_id == user_id).all()
    return jsonify([
        {
            'id': m.id,
            'serial_number': m.serial_number,
            'model': m.model,
            'color': m.color
        } for m in markers
    ])

@marker_bp.route('/marker/toggle-stolen', methods=['POST'])
def toggle_stolen():
    data = request.json
    marker = Marker.query.filter_by(serial_number=data['serial_number']).first()
    if not marker:
        return jsonify({'message': 'Marker not found'}), 404

    marker.status = 'stolen' if marker.status != 'stolen' else 'active'
    db.session.commit()
    return jsonify({'message': 'Marker status updated', 'status': marker.status})


