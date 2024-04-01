from flask_sqlalchemy import SQLAlchemy
from models.user import db,User
from flask import Flask, render_template, request, redirect
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

    return render_template('register.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
