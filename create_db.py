from app import app
from extensions import db

from models.user import User
from models.student import Student
from models.attendance import Attendance

with app.app_context():
    db.create_all()
    print("Database tables created!")