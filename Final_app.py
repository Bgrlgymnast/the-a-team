import streamlit as st
import joblib
import pandas as pd
import sklearn
print(sklearn.__version__)

# Load the trained models
multi_output_classifier = joblib.load('multi_output_classifier.pkl')
multi_output_regressor = joblib.load('multi_output_regressor.pkl')

# Streamlit app title
st.title("Predict GDP, Population Growth, and More")

# Input form for BDay, BMonth, and Party
bday = st.number_input('Enter your Birth Day:', min_value=1, max_value=31, step=1)
bmonth = st.number_input('Enter your Birth Month:', min_value=1, max_value=12, step=1)
party = st.selectbox('Select your Party:', ['Democrat', 'Republican', 'Other'])

# Map party to encoded values (based on how they were encoded in your model)
party_map = {'Democrat': 0, 'Republican': 1, 'Other': 2}
party_encoded = party_map[party]

# Prepare input data for the model
input_data = pd.DataFrame({
    'BDay': [bday],
    'BMonth': [bmonth],
    'Party': [party_encoded]
})

# Make predictions when the button is clicked
if st.button('Predict'):
    # Predict categorical values (e.g., sign, VP, Name)
    y_pred_categorical = multi_output_classifier.predict(input_data)
    # Predict continuous values (e.g., GDP Growth, Population Growth)
    y_pred_continuous = multi_output_regressor.predict(input_data)

    # Display predictions for categorical outputs
    sign, vp, name = y_pred_categorical[0]
    st.write(f"Predicted Sign: {sign}")
    st.write(f"Predicted VP: {vp}")
    st.write(f"Predicted Name: {name}")

    # Display predictions for continuous outputs
    gdp_growth, population_growth, gdp_percent_growth, population_percent_growth = y_pred_continuous[0]
    st.write(f"Predicted GDP Growth: {gdp_growth:.2f}")
    st.write(f"Predicted Population Growth: {population_growth:.2f}")
    st.write(f"Predicted GDP Percent Growth: {gdp_percent_growth:.2f}")
    st.write(f"Predicted Population Percent Growth: {population_percent_growth:.2f}")
