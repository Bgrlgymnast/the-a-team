import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the pre-trained model
model = joblib.load('GDP_President_VP_model.pkl')
data = pd.read_csv('dummy_df-94.csv')  # Load your dataset for President and VP info

# Define the app layout
st.title('GDP Growth, President, and VP Predictor')

# Input fields for the user to provide their data
party = st.selectbox('Select Political Party', ['Independent', 'Democrat', 'Republican'])
bday = st.slider('Select your Birthday (day of month)', 1, 31)

# Convert the party input to match the one-hot encoding used in the dataset
party_features = {
    'Independent': [0, 0, 0, 1, 0, 0, 0],  # Corresponds to Party_Independent
    'Democrat': [1, 0, 0, 0, 0, 0, 0],     # Corresponds to Party_Democrat
    'Republican': [0, 0, 0, 0, 0, 1, 0]    # Corresponds to Party_Republican
}

# Create a full feature array with default values for all other columns
input_data = np.zeros((1, 94))  # Adjust based on the number of features in the model (94)

# Place BDay into the appropriate column (assuming BDay is the second column in your data)
input_data[0, 1] = bday  # Index 1 corresponds to BDay

# Place the party features in the correct columns (adjusted to match correct length)
# Assuming the last 7 columns are for the political parties
input_data[0, -7:] = party_features[party]

# Button for Predicting GDP Growth, President, and VP
if st.button('Predict GDP Growth, President, and VP'):
    # Make prediction using the model
    prediction = model.predict(input_data)
    
    # Debugging to show the raw predictions
    st.write(f'Raw model predictions: {prediction}')

    # Assume the prediction structure is [GDP Growth, President, Vice President]
    predicted_gdp_growth = prediction[0][0]  # First value is GDP growth
    president_prediction = prediction[0][1]  # Second value is President
    vp_prediction = prediction[0][2]         # Third value is Vice President
    
    # Extract the president and VP columns
    president_columns = data.columns[data.columns.str.startswith('Name_')]
    vp_columns = data.columns[data.columns.str.startswith('VP_')]

    # Find the predicted president and VP by checking which column has the value 1 (True)
    predicted_president = president_columns[np.argmax(president_prediction)] if np.any(president_prediction) else 'Unknown President'
    predicted_vp = vp_columns[np.argmax(vp_prediction)] if np.any(vp_prediction) else 'Unknown Vice President'

    # Display the predicted names (strip the 'Name_' and 'VP_' prefix for clarity)
    st.write(f'Predicted GDP Growth: {predicted_gdp_growth}')
    st.write(f'Predicted President: {predicted_president.replace("Name_", "")}')
    st.write(f'Predicted Vice President: {predicted_vp.replace("VP_", "")}')
