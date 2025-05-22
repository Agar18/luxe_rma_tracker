from app import db

class Ownership(db.Model):
    __tablename__ = 'ownerships'

    id = db.Column(db.Integer, primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('markers.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    ownership_start = db.Column(db.Date, nullable=False)
    ownership_end = db.Column(db.Date)
    purchased_from = db.Column(db.Text)
    purchase_date = db.Column(db.Date)
