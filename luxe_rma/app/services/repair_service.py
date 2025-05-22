from app import db
from app.models.repair import Repair
from datetime import datetime

def log_repair(data):
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
    return repair
