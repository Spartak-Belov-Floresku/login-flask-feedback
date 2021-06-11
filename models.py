from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, sql
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)


    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """register user with hashed password and reter user object"""

        password_hash = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) str
        password_utf8_hash = password_hash.decode("utf8")

        #return user obj
        return cls(username=username, password=password_utf8_hash, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """validate if user exits and password matches"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False


class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    username = db.Column(db.String(20), db.ForeignKey('users.username'), primary_key=True, nullable=False)
