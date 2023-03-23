from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect model to Flask app. Function called in app.py"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model for site user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    favorite = db.relationship('FavoritePark', backref='user')

    collected = db.relationship('CollectedPark', backref='user')

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

    @classmethod
    def register(cls, username, password, email, first, last):
        """Register user w/ hashed password & return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')

        return cls(username=username, password=hashed_utf8, email=email, first_name=first, last_name=last)
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct
        Return user if valid; else return False"""

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class FavoritePark(db.Model):
    """Model for favorite parks"""

    __tablename__ = 'favorite_parks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    park_code = db.Column(db.Text, nullable=False)
    park_name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class CollectedPark(db.Model):
    """Model for collected parks"""

    __tablename__ = 'collected_parks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    park_code = db.Column(db.Text, nullable=False)
    park_name = db.Column(db.Text, nullable=False)
    state_code = db.Column(db.String(2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


