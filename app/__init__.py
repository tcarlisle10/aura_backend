from flask import Flask
from app.models import db
from app.extensions import ma
from app.blueprints.users import users_bp
from dotenv import load_dotenv
import os

load_dotenv()

def create_app(config_name="config.DevelopmentConfig"):
    # Create the Flask app 
    app = Flask(__name__) 
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True" 
    
    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(users_bp, url_prefix="/users")
    
    return app