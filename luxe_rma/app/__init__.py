from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    CORS(app)  # Allow cross-origin for API frontend

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.marker import marker_bp
    from app.routes.rma import rma_bp
    from app.routes.repair import repair_bp
    from app.routes.notify import notify_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(marker_bp, url_prefix='/marker')
    app.register_blueprint(rma_bp, url_prefix='/rma')
    app.register_blueprint(repair_bp, url_prefix='/repair')
    app.register_blueprint(notify_bp, url_prefix='/notify')

    return app
