from app import db

class MarkerEvent(db.Model):
    __tablename__ = 'marker_events'

    id = db.Column(db.Integer, primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('markers.id', ondelete='CASCADE'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
