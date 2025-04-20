from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .routes import init_routes
from .db import init_db
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    csrf = CSRFProtect(app)
    
    init_routes(app)
    with app.app_context():
        init_db()
    
    return app