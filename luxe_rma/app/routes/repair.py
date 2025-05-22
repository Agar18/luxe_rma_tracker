from flask import Blueprint, request, jsonify
from app import db
from app.models.repair import Repair
from datetime import datetime

repair_bp = Blueprint('repair', __name__)

@repair_bp.route('/log', methods=['POST'])
def log_repair():
    data = request.json

    repair = Repair(
        marker_id=data['marker_id'],
        tech_id=data['tech_id'],
        description=data['description'],
        diagnosis=data['diagnosis'],
        repair_date=datetime.strptime(data['repair_date'], '%Y-%m-%d'),
        cost=data['cost'],
        warranty=data['warranty'],
        status=data['status']
    )
    db.session.add(repair)
    db.session.commit()
    return jsonify({'message': 'Repair logged'}), 201

@repair_bp.route('/history/<int:marker_id>', methods=['GET'])
def repair_history(marker_id):
    repairs = Repair.query.filter_by(marker_id=marker_id).all()
    return jsonify([
        {
            'description': r.description,
            'diagnosis': r.diagnosis,
            'repair_date': str(r.repair_date),
            'cost': float(r.cost),
            'status': r.status
        }
        for r in repairs
    ])
