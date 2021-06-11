from models import db, User, Feedback
from app import app

"""creat table"""
db.drop_all()
db.create_all()

"""if table is not empty"""
User.query.delete()
Feedback.query.delete()
