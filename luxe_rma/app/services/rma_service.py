import uuid
from datetime import datetime
from app import db
from app.models.rma import RMA

def create_rma(marker_id, user_id):
    rma_number = f"RMA-{uuid.uuid4().hex[:8].upper()}"
    new_rma = RMA(
        marker_id=marker_id,
        user_id=user_id,
        rma_number=rma_number,
        created_at=datetime.utcnow(),
        status='open'
    )
    db.session.add(new_rma)
    db.session.commit()
    return new_rma
