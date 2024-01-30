# Load necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib

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
    sim_scores = sim_scores[1:20]  # Get top recommendations
    airbnb_indices = [i[0] for i in sim_scores]
    
    recommendations = []
    for idx in airbnb_indices:
        recommendation = {
            'name': airbnb_df['name'].iloc[idx],
            'ratings': airbnb_df['ratings'].iloc[idx],
            'price': airbnb_df['price'].iloc[idx]
        }
        recommendations.append(recommendation)
    
    return recommendations

# Example usage:
theme_input = "City"
neighborhood_input = "Nairobi"
recommendations = get_recommendations(theme_input, neighborhood_input)
for idx, recommendation in enumerate(recommendations, 1):
    print(f"Recommendation {idx}: {recommendation['name']} - Ratings: {recommendation['ratings']}, Price: {recommendation['price']}")
