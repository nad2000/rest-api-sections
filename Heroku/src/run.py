import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

