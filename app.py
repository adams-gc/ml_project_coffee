from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import database

# Initialize the Flask app
app = Flask(__name__)

# Load the data
df = pd.read_csv('coffee_data.csv')

# Encode categorical features
def encode_feature(df, feature):
    encoder = LabelEncoder()
    encoder.fit(df[feature].apply(str).str.capitalize())
    return encoder, encoder.transform(df[feature].apply(str).str.capitalize())

# Encode dataset
encoders = {}
for feature in ['Roast Level', 'Acidity', 'Drink Type', 'Description', 'Drink Time', 'Strength']:
    encoder, encoded_feature = encode_feature(df, feature)
    df[feature + '_Encoded'] = encoded_feature
    encoders[feature] = encoder

# Encode user input
def encode_user_input(user_input, feature, encoders):
    encoder = encoders[feature]
    user_input_cleaned = user_input.capitalize()
    if user_input_cleaned in encoder.classes_:
        return encoder.transform([user_input_cleaned])[0]
    else:
        return None

# Debug route to test if the server is working
@app.route('/')
def home():
    return render_template('index.html')

# Recommendation route
@app.route('/recommend', methods=['POST'])
def recommend():
    # Collect user input from request body
    user_data = request.json



    user_roast =  user_data.get('roast_level', '').lower()  # Convert to lowercase
    user_acidity =  user_data.get('acidity', '').lower()  # Convert to lowercase
    user_drink =  user_data.get('drink_type', '').lower()  # Convert to lowercase
    user_ideal_cup =  user_data.get('description', '').lower()  # Convert to lowercase
    user_drink_time =  user_data.get('drink_time', '').lower()  # Convert to lowercase
    user_strength =  user_data.get('strength', '').lower()  # Convert to lowercase

    # Define valid labels for each category
    valid_roast_levels = ['light', 'medium', 'dark']
    valid_acidities = ['low', 'medium', 'high']
    valid_drink_types = ['espresso', 'drip', 'cold brew', 'latte']
    valid_ideal_cups = ['nutty', 'fruity', 'floral', 'chocolatey']
    valid_drink_times = ['morning', 'afternoon', 'evening', 'night']
    valid_strengths = ['mild', 'medium', 'strong']




    if not user_data:
        return jsonify({"error": "No data received!"}), 400

    # Encode user input
    user_roast = encode_user_input(user_data.get('roast_level', ''), 'Roast Level', encoders)
    user_acidity = encode_user_input(user_data.get('acidity', ''), 'Acidity', encoders)
    user_drink = encode_user_input(user_data.get('drink_type', ''), 'Drink Type', encoders)
    user_ideal_cup = encode_user_input(user_data.get('description', ''), 'Description', encoders)
    user_drink_time = encode_user_input(user_data.get('drink_time', ''), 'Drink Time', encoders)
    user_strength = encode_user_input(user_data.get('strength', ''), 'Strength', encoders)

    # Validate user input
    if None in [user_roast, user_acidity, user_drink, user_ideal_cup, user_drink_time, user_strength]:
        return jsonify({"error": "Some of your inputs are not recognized. Please use the specified labels."}), 400

    # Create feature vector for user preferences
    user_vector = np.array([user_roast, user_acidity, user_drink, user_ideal_cup, user_drink_time, user_strength])
    user_df = pd.DataFrame([user_vector], columns=[f + '_Encoded' for f in ['Roast Level', 'Acidity', 'Drink Type', 'Description', 'Drink Time', 'Strength']])

    # Compute similarity
    user_similarity = cosine_similarity(user_df, df[[f + '_Encoded' for f in ['Roast Level', 'Acidity', 'Drink Type', 'Description', 'Drink Time', 'Strength']]])
    df['Similarity'] = user_similarity.flatten()

    # Dimensionality reduction with SVD
    svd = TruncatedSVD(n_components=2)
    df_svd = svd.fit_transform(df[[f + '_Encoded' for f in ['Roast Level', 'Acidity', 'Drink Type', 'Description', 'Drink Time', 'Strength']]])
    user_vector_svd = svd.transform(user_df)

    # Compute SVD-based similarity
    user_similarity_svd = cosine_similarity(user_vector_svd, df_svd)
    df['Similarity_SVD'] = user_similarity_svd.flatten()

    # Recommend the top result
    top_recommendation = df.sort_values(by='Similarity_SVD', ascending=False).head(1)

    # Save user input and recommendation ID to the database
    recommendation_id = top_recommendation.index[0]
    store_user_input(user_data, recommendation_id)

    # Return the recommendation
    recommendation = top_recommendation[['Flavor', 'Roast Level', 'Acidity', 'Drink Type', 'Country', 'Health Benefit', 'Description', 'Video URL']].to_dict(orient='records')[0]
    
    return render_template('recommendation.html', recommendation=recommendation)

# Function to store user input in the database
def store_user_input(user_data, recommendation_id):
    conn = database.get_db_connection()
    conn.execute('''
        INSERT INTO feedback (roast_level, acidity, drink_type, description, drink_time, strength, recommendation_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_data['roast_level'], user_data['acidity'], user_data['drink_type'],
          user_data['description'], user_data['drink_time'], user_data['strength'], recommendation_id))
    conn.commit()
    conn.close()

# Route for handling feedback
@app.route('/feedback', methods=['POST'])
def feedback():
    recommendation_id = request.form.get('recommendation_id')
    feedback_value = request.form.get('feedback')

    if not recommendation_id or not feedback_value:
        return jsonify({"error": "Missing feedback or recommendation ID."}), 400

    # Store feedback in the database
    store_feedback(recommendation_id, feedback_value)

    return redirect('/thank_you')

# Function to store feedback in the database
def store_feedback(recommendation_id, feedback_value):
    conn = database.get_db_connection()
    conn.execute('''
        UPDATE feedback SET feedback_value = ?
        WHERE recommendation_id = ?
    ''', (feedback_value, recommendation_id))
    conn.commit()
    conn.close()

# Test route
@app.route('/test')
def test_recommend():
    return jsonify({"message": "Test route for recommendations!"})

# Thank you route
@app.route('/thank_you')
def thank_you():
    return "Thank you for your feedback!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
