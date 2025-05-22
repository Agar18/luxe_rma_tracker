from sqlalchemy import text
from app import create_app, db

app = create_app()

with app.app_context():
    try:
        result = db.session.execute(text('SELECT 1'))
        print("✅ Database connection successful. Result:", result.scalar())
    except Exception as e:
        print("❌ Database connection failed:", str(e))