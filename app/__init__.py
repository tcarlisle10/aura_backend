from flask import Flask
from flask_migrate import Migrate
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
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "/path/to/upload/folder")
    app.config["SECRET_KEY"] = os.getenv


    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)


    app.register_blueprint(users_bp, url_prefix="/users")
    
    return app