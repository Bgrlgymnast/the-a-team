import streamlit as st
import numpy as np
import pandas as pd
import joblib  # For loading the saved model
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize Streamlit app
st.title("Presidential Outcome Predictor")

# Load the saved model (replace 'model_path.pkl' with the actual path)
model = joblib.load('C:/Users/dell/Documents/GitHub/the-a-team/model4-95.ipynb')

# Load and preprocess data if required (e.g., features like economy, polling, etc.)
# Depending on what the notebook uses, you might need to adjust preprocessing here.
# For demonstration, we're using some placeholder sample data.

X_train = pd.DataFrame({
    'region': ['north', 'south', 'east', 'west', 'midwest'],
    'economy_index': [50, 40, 55, 60, 48],
    'polling_percentage': [45, 55, 60, 50, 47],
    'candidate1_advantage': [1, 0, 1, 0, 1]
})

y_train = pd.DataFrame({
    'outcome_win': [1, 0, 1, 0, 1],  # 1: Win, 0: Loss
    'electoral_votes': [270, 250, 320, 200, 275]
})

# Initialize vectorizer for text features like regions (adjust based on your notebook features)
vectorizer = TfidfVectorizer()

# Standardize the numerical features (adjust to match the features in your model)
scaler = StandardScaler()
X_train[['economy_index', 'polling_percentage']] = scaler.fit_transform(X_train[['economy_index', 'polling_percentage']])

# Vectorize and combine with other features (this is simplified; adjust as per notebook's feature engineering)
X_train_region_vectorized = vectorizer.fit_transform(X_train['region'])
X_train_combined = np.hstack([X_train_region_vectorized.toarray(), X_train[['economy_index', 'polling_percentage', 'candidate1_advantage']].values])

# User input for region
input_region = st.text_input("Enter the region (north, south, east, west, midwest)", "")

# User input for economy and polling data
default_economy_index = st.slider("Enter the economy index (scale 0-100)", 0, 100, 50)
default_polling_percentage = st.slider("Enter the polling percentage for Candidate 1", 0, 100, 50)
default_candidate_advantage = st.radio("Is Candidate 1 in advantage?", (0, 1))

# Button to trigger the prediction
if st.button("Predict"):
    if input_region:
        # Vectorize the input region
        input_region_vectorized = vectorizer.transform([input_region])

        # Standardize the input features
        input_combined_features = scaler.transform([[default_economy_index, default_polling_percentage]])

        # Combine region vector with the standardized numerical features
        input_combined = np.hstack([input_region_vectorized.toarray(), input_combined_features, [[default_candidate_advantage]]])

        # Make the prediction using the loaded model
        y_pred_new = model.predict(input_combined)

        # Display the prediction result
        st.write("Predicted Outcome (1: Win, 0: Loss):", y_pred_new[0][0])
        st.write("Predicted Electoral Votes:", y_pred_new[0][1])
    else:
        st.write("Please enter a valid region.")
