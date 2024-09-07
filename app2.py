import streamlit as st
import joblib
import numpy as np

# Load the pre-trained models
model = joblib.load('model4-95-test.pkl')  # Classification model
model2 = joblib.load('GDP_growth_regression_model.pkl')  # Regression model

# Define the app layout
st.title('GDP Growth Predictor')

# Input fields for the user to provide their data
party = st.selectbox('Select Political Party', ['Independent', 'Democrat', 'Republican'])
bday = st.slider('Select your Birthday (day of month)', 1, 31)

# # Convert the party input to match the one-hot encoding used in the dataset (7 party columns)
# party_features = {
#     'Independent': [0, 0, 0, 1, 0, 0, 0],  # Party_Independent
#     'Democrat': [1, 0, 0, 0, 0, 0, 0],  # Party_Democrat
#     'Republican': [0, 0, 0, 0, 0, 1, 0]  # Party_Republican
# }

# Create a full feature array with default values for all other columns
input_data = np.zeros((1, 97))  # 98 features based on the actual dataset

# Place BDay into the appropriate column (which is the 2nd column in the dataset)
input_data[0, 1] = bday  # Index 1 corresponds to BDay

# Place the party features into the correct positions based on their column positions in the dataset
# Party columns are at positions 90 to 96
# input_data[0, 88:95] = party_features[party]  # Adjust indices for the party columns

# Make the predictions when the button is pressed
if st.button('Predict GDP Growth'):
    # Prediction using the classification model (model)
    growth_prediction = model.predict(input_data)
    growth_result = "Yes" if growth_prediction[0] == 1 else "No"
    
    # Prediction using the regression model (model2) for GDP growth percentage
    gdp_growth_percent = model2.predict(input_data)[0]  # Only predict for one instance
    
    # Display results
    st.write(f'Will there be GDP Growth? {growth_result}')
    st.write(f'Predicted GDP Growth Percentage: {gdp_growth_percent[0]:.2f}%')
