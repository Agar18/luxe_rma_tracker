from app import db

class Marker(db.Model):
    __tablename__ = 'markers'
    
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50), unique=True, nullable=False)
    model = db.Column(db.String(50))
    color = db.Column(db.String(50))
    date_made = db.Column(db.Date)
    photo_url = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, stolen, etc.
