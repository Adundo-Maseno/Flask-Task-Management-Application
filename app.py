from flask_sqlalchemy import SQLAlchemy
from models.user import db,User
from flask import Flask, render_template, request, redirect,session,url_for
from flask.config import T


# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'movitech'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize SQLAlchemy
db.init_app(app)

# Create the database and tables
with app.app_context():
    db.create_all()

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

# Route for user registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
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

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # If the user exists and the password is correct, log in the user
            session['user_id'] = user.id
            return 'Logged in successfully!'
        else:
            # If the user does not exist or the password is incorrect, show an error message
            return 'Invalid username or password!'

    return render_template('index.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
