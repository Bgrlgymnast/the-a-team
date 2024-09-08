import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load the model and dataset
model = joblib.load("trained_presidential_model.pkl")
data = pd.read_csv("dummy_df-94.csv")

# Initialize Streamlit app
st.title("GDP and President Predictor with Model")

# User input for BDay and political party
input_bday = st.number_input("Enter the Birth Day", min_value=1, max_value=31, step=1)
input_party = st.selectbox(
    "Select the Political Party", 
    ["Democrat", "Republican", "Independent", "Democratic-Republican", "Federalist", "National Union", "Whig"]
)

# Button to trigger the prediction
if st.button("Predict"):
    # Step 1: Map party to boolean format used in the dataset
    party_column = f"Party_{input_party}"

    # Step 2: Filter data to create a valid input row for the model
    input_row = data[(data['BDay'] == input_bday) & (data[party_column] == True)].copy()
    
    if not input_row.empty:
        # Step 3: Drop unnecessary columns, keeping only the features the model needs
        # Adjust the columns based on what the model expects
        model_input = input_row.drop(columns=["Year", "GDP Growth", "Population Growth", "GDP Percent Growth", "Population Percent Growth"])
        
        # Ensure the input is in the correct shape (2D array)
        input_data = model_input.values.reshape(1, -1)

        # Step 4: Make predictions using the loaded model
     

