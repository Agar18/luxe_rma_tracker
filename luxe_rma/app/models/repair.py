from app import db

class Repair(db.Model):
    __tablename__ = 'repairs'

    id = db.Column(db.Integer, primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('markers.id', ondelete='CASCADE'))
    tech_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    description = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    repair_date = db.Column(db.Date)
    cost = db.Column(db.Numeric(10, 2))
    warranty = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20))
