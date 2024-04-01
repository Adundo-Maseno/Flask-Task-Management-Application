from flask_sqlalchemy import SQLAlchemy
from models.user import db, User
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'movitech'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize SQLAlchemy
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'  # Specify the login view

# Create the database and tables
with app.app_context():
    db.create_all()

# Define routes
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['regEmail']
    password = request.form['regPassword']
    confirm_password = request.form['confirmPassword']

    # Check if passwords match
    if password != confirm_password:
        return 'Passwords do not match!'

    # Check if username or email already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return 'Username already exists!'

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return 'Email already exists!'

    # Create a new user
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return 'User registered successfully!'

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Check if the user exists in the database
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # If the user exists and the password is correct, log in the user
        login_user(user)
        return redirect(url_for('index'))
    else:
        # If the user does not exist or the password is incorrect, show an error message
        return 'Invalid email or password!'

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
