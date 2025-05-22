from app import db

class RMA(db.Model):
    __tablename__ = 'rmas'

    id = db.Column(db.Integer, primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('markers.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    rma_number = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime)
    tracking_number = db.Column(db.String(100))
    approved_cost = db.Column(db.Numeric(10, 2))
    payment_status = db.Column(db.String(20), default='unpaid')
