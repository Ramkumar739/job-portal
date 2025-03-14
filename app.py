from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import _mysql_connector


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flask_user:Ram2003@localhost/user_auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100),unique=True,nullable = False)
    password = db.Column(db.String(200), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Sign Up Route
@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()  # Get JSON data from the request
    username = data['username']
    email = data['email']
    password = data['password']
    # hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 200
    except:
        db.session.rollback()
        return {'message': 'User already exists!'}, 400

# Login Route
# Login Route
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()  # Parse JSON data
    email = data['email']
    password = data['password']
    
    user = User.query.filter_by(email=email).first()  # Find user by username (email)
    if user:
        # Log the hashed password stored in the database and the entered password
        print(f"Stored hashed password: {user.password}")
        print(f"Entered password: {password}")

        # Compare the entered password with the hashed password stored in the database
        if user.password == password:
            return {'message': 'Login successful'}, 200  # Successful login
        else:
            return {'message': 'Invalid username or password'}, 401  # Incorrect password
    else:
        return {'message': 'Invalid username or password'}, 401  # User not found
    

@app.route("/index")
def welcome():
    return "Welcome to the protected page!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5500, debug=True)
