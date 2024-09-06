import streamlit as st
import numpy as np
import pandas as pd
import joblib  # For loading the saved model
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize Streamlit app
st.title("Presidential Outcome Predictor")

# Load the saved model, vectorizer, and scaler
model = joblib.load("trained_presidential_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
scaler = joblib.load("scaler.pkl")

# User input for region
input_region = st.text_input("Enter the region (north, south, east, west, midwest)", "")

# User input for economy and polling data
default_economy_index = st.slider("Enter the economy index (scale 0-100)", 0, 100, 50)
default_polling_percentage = st.slider("Enter the polling percentage for Candidate 1", 0, 100, 50)
default_candidate_advantage = st.radio("Is Candidate 1 in advantage?", (0, 1))

# Button to trigger the prediction
if st.button("Predict"):
    if input_region and input_region in vectorizer.vocabulary_:
        # Vectorize the input region
        input_region_vectorized = vectorizer.transform([input_region])

        # Standardize the input features
        input_combined_features = scaler.transform([[default_economy_index, default_polling_percentage]])

        # Combine region vector with the standardized numerical features
        input_combined = np.hstack([input_region_vectorized.toarray(), input_combined_features, [[default_candidate_advantage]]])

        # Make the prediction using the loaded model
        y_pred_new = model.predict(input_combined)
        y_prob_new = model.predict_proba(input_combined)

        # Display the prediction result
        st.write("Predicted Outcome (1: Win, 0: Loss):", y_pred_new[0][0])
        st.write("Predicted Electoral Votes:", y_pred_new[0][1])

        # Display probability
        st.write("Probability of Win:", y_prob_new[0][1])
        st.write("Probability of Loss:", y_prob_new[0][0])
    else:
        st.write("Please enter a valid region.")
