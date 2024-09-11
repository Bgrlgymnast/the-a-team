import streamlit as st
import joblib
import pandas as pd
from PIL import Image
import os

# Get directory
current_dir = os.getcwd()
if "final_app" not in current_dir:
    current_dir = os.path.join(current_dir, 'final_app')

# Load the trained models
multi_output_classifier = joblib.load(os.path.join(current_dir, 'multi_output_classifier.pkl'))
multi_output_regressor = joblib.load(os.path.join(current_dir, 'multi_output_regressor.pkl'))

# Load the label encoders for categorical columns
sign_encoder = joblib.load(os.path.join(current_dir, 'sign_encoder.pkl'))
vp_encoder = joblib.load(os.path.join(current_dir, 'VP_encoder.pkl'))
name_encoder = joblib.load(os.path.join(current_dir, 'Name_encoder.pkl'))

# Path to the folder with president images
image_folder = 'Pres_pic/'

# Streamlit app title
st.title("How Would you Fare as President? A Horoscope Outlook")

# Input form for BDay, BMonth, and Party
bday = st.number_input('Enter your Birth Day:', min_value=1, max_value=31, step=1)
bmonth = st.number_input('Enter your Birth Month:', min_value=1, max_value=12, step=1)
party = st.selectbox('Select your Party:', ['Democrat', 'Republican', 'Other'])

# Map party to encoded values (based on how they were encoded in your model)
party_map = {'Democrat': 0, 'Republican': 1, 'Other': 2}
party_encoded = party_map[party]

# Prepare input data for the model
input_data = pd.DataFrame({
    'bday': [bday],
    'bmonth': [bmonth],
    'party': [party_encoded]
})

# Make predictions when the button is clicked
if st.button('Predict'):
    # Predict categorical values (e.g., sign, VP, Name)
    y_pred_categorical = multi_output_classifier.predict(input_data)
    # Predict continuous values (e.g., GDP Growth, Population Growth)
    y_pred_continuous = multi_output_regressor.predict(input_data)

    # Decode the categorical predictions
    sign = sign_encoder.inverse_transform([y_pred_categorical[0][0]])[0]
    vp = vp_encoder.inverse_transform([y_pred_categorical[0][1]])[0]
    name = name_encoder.inverse_transform([y_pred_categorical[0][2]])[0]
  
   # Display the corresponding president's picture
    image_path = os.path.join(current_dir, image_folder, f"{name}.jpg")
    if os.path.exists(image_path):
        img = Image.open(image_path)
        st.image(img, caption=f"You are most like {name}", use_column_width=True)
     # Add a larger caption for the president's name
        st.markdown(f"<h2 style='text-align: center;'>{name}</h2>", unsafe_allow_html=True)
    else:
        st.write("Sorry, we couldn't find an image for this president.")
   
    # Display predictions for categorical outputs
    st.write(f"You would most likely be {sign}.")
    
    if vp == "office vacant":
        st.write("You would get along best with NO ONE as your VP.")
    else:
        st.write(f"You would get along best with {vp} as your VP.")

    # Display predictions for continuous outputs
    gdp_growth, population_growth, gdp_percent_growth, population_percent_growth = y_pred_continuous[0]

    # Conditional check for whether the economy is on the upswing
    if gdp_growth > 0:
        st.write("Will the economy be on the upswing?: Yes")
    else:
        st.write("Will the economy be on the downswing?: No")

    # Display other continuous outputs
    st.write(f"GDP Percent Growth: {gdp_percent_growth*100:.2f}%")

    # Conditional check for population growth
    if population_growth > 0:
        st.write("Would you be a babymaker?: Yes")
    else:
        st.write("Would you be a babymaker?: No")

    st.write(f"Population Percent Growth: {population_percent_growth*100:.2f}%")