from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Hashes the password before saving it to the database."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the hashed password."""
        return check_password_hash(self.password_hash, password)

    # Required methods for Flask-Login
    def get_id(self):
        """Returns the user ID as a string."""
        return str(self.id)

    @property
    def is_authenticated(self):
        """Returns True if the user is authenticated, i.e., they have provided valid credentials."""
        return True

    @property
    def is_active(self):
        """Returns True if the user's account is active."""
        return True

    @property
    def is_anonymous(self):
        """Returns True if the current user is an anonymous user."""
        return False
