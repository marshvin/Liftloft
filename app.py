from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib

app = Flask(__name__)

# Load the cleaned DataFrame
cleaned_data_path = 'cleaned_data.csv'
airbnb_df = pd.read_csv(cleaned_data_path)

# Load the saved model
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
cosine_sim = joblib.load('cosine_sim.pkl')
tfidf_matrix = tfidf_vectorizer.transform(airbnb_df['theme'])

# Function to get recommendations based on user input
def get_recommendations(theme):
    theme_vectorized = tfidf_vectorizer.transform([theme])
    cosine_scores = linear_kernel(theme_vectorized, tfidf_matrix).flatten()
    sim_scores = list(enumerate(cosine_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:20]  # Get top recommendations
    airbnb_indices = [i[0] for i in sim_scores]
    return airbnb_df['name'].iloc[airbnb_indices].tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['theme']
    recommendations = get_recommendations(user_input)
    return render_template('recommendation.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib

app = Flask(__name__)

# Load the cleaned DataFrame
cleaned_data_path = 'cleaned_data.csv'
airbnb_df = pd.read_csv(cleaned_data_path)

# Load the saved model
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
cosine_sim = joblib.load('cosine_sim.pkl')
tfidf_matrix = tfidf_vectorizer.transform(airbnb_df['theme'])

# Function to get recommendations based on user input
def get_recommendations(theme):
    theme_vectorized = tfidf_vectorizer.transform([theme])
    cosine_scores = linear_kernel(theme_vectorized, tfidf_matrix).flatten()
    sim_scores = list(enumerate(cosine_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:20]  # Get top recommendations
    airbnb_indices = [i[0] for i in sim_scores]
    return airbnb_df['name'].iloc[airbnb_indices].tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['theme']
    recommendations = get_recommendations(user_input)
    return render_template('recommendation.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
