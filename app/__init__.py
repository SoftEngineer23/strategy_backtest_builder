"""
Flask App Factory
Application factory for the Strategy Builder API.
"""

from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()


def create_app(config_name=None):
    """Create and configure the Flask app"""
    app = Flask(__name__)

    # Load config
    app.config.from_object(get_config(config_name))

    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


def get_config(config_name):
    from app.config import config_map
    return config_map.get(config_name or os.getenv('FLASK_ENV', 'development'))