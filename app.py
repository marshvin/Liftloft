from flask import Flask, render_template, make_response, jsonify, request, session
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

# Load the cleaned DataFrame
cleaned_data_path = 'cleaned_data.csv'
airbnb_df = pd.read_csv(cleaned_data_path)

# Load the saved model
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
cosine_sim_train = joblib.load('cosine_sim_train.pkl')
tfidf_matrix_train = tfidf_vectorizer.transform(airbnb_df['theme'] + ' ' + airbnb_df['neighborhood'])

# Function to get recommendations based on theme and neighborhood
def get_recommendations(theme, neighborhood):
    input_text = f"{theme} {neighborhood}"
    theme_vectorized = tfidf_vectorizer.transform([input_text])
    cosine_scores = linear_kernel(theme_vectorized, tfidf_matrix_train).flatten()
    sim_scores = list(enumerate(cosine_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:40]  # Get top recommendations
    airbnb_indices = [i[0] for i in sim_scores]
    
    recommendations = []
    for idx in airbnb_indices:
        recommendation = {
            'name': airbnb_df['name'].iloc[idx],
            #'image_url': airbnb_df['image_url'].iloc[idx],
            'ratings': airbnb_df['ratings'].iloc[idx],
            'price': airbnb_df['price'].iloc[idx]
        }
        recommendations.append(recommendation)
    
    return recommendations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input_theme = request.form['theme']
    user_input_neighborhood = request.form['location']
    
    recommendations = get_recommendations(user_input_theme, user_input_neighborhood)
    
    return render_template('recommendation.html', recommendations=recommendations)

# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = '7KXn3mXuciicTDlr2f8ooJCWBEW9iRXO'
# database name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/Liftloft'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object
db = SQLAlchemy(app)
  
# Database ORMs
class User(db.Model):
    __tablename__ = 'User'  # Specify the correct table name here
    # Define other columns...
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(80))

class Airbnb(db.Model):
    __tablename__ = 'airbnb'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    theme = db.Column(db.String(100))
    location = db.Column(db.String(100))
    ratings = db.Column(db.Float)
    price = db.Column(db.Float)
    image_url = db.Column(db.String(200))  # Store image URLs  
# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated
  
# Route for the upload page and handling image uploads
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        name = request.form['name']
        theme = request.form['theme']
        location = request.form['location']
        ratings = float(request.form['ratings'])
        price = float(request.form['price'])
        
        # Handle image upload to AWS S3
        if 'image' in request.files:
            image = request.files['image']
            # Process the uploaded image (e.g., save to disk, upload to S3)
            # Store the image URL in the database
            # Example: image_url = upload_image_to_s3(image)
            image_url = 'url_of_uploaded_image'
        
        
            airbnb = Airbnb(name=name, theme=theme, location=location, ratings=ratings, price=price)
            db.session.add(airbnb)
            db.session.commit()
        
        return f"Airbnb listing uploaded successfully. Image URL: {image_url}"
    return "Unsupported HTTP method."

# Define the signup and signin routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Process the form data
        data = request.form
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return make_response('User already exists. Please Log in.', 202)

        # Create a new user
        new_user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password)
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return make_response('Successfully registered.', 201)

    # Render the signup page if the request method is GET
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Process the form data
        auth = request.form
        email = auth.get('email')
        password = auth.get('password')

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return make_response('Could not verify', 403)

        # Create a session for the user
        session['user_id'] = user.id

        return make_response(jsonify({'message': 'Login successful.'}), 200)

    # Render the signin page if the request method is GET
    return render_template('signin.html')

@app.route('/booking')
def booking():
    # Retrieve data from query parameters
    name = request.args.get('name')
    price = request.args.get('price')
    image_url = request.args.get('image_url')
    
    # Render booking page with data
    return render_template('booking.html', name=name, price=price, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)