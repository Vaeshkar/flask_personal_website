from flask import Flask
from .routes import admin_bp, auth_bp, home_bp
from .config import BaseConfig
from dotenv import load_dotenv
load_dotenv()
 
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = BaseConfig.SECRET_KEY
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
 
    return app