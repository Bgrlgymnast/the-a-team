import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the pre-trained model and dataset
model = joblib.load('GDP_growth_percent.pkl')
data = pd.read_csv('dummy_df-94.csv')  # Load your dataset for President and VP info

# Define the app layout
st.title('GDP Growth Predictor')

# Input fields for the user to provide their data
party = st.selectbox('Select Political Party', ['Independent', 'Democrat', 'Republican'])
bday = st.slider('Select your Birthday (day of month)', 1, 31)

# Convert the party input to match the one-hot encoding used in the dataset
party_features = {
    'Independent': [0, 0, 0, 1, 0, 0, 0],  # Independent
    'Democrat': [1, 0, 0, 0, 0, 0, 0],  # Democrat
    'Republican': [0, 0, 0, 0, 1, 0, 0]  # Republican
}

# Create a full feature array with default values for all other columns
input_data = np.zeros((1, 97))  # Adjust based on the number of features in the model

# Place BDay into the appropriate column (assuming BDay is the second column in your data)
input_data[0, 1] = bday  # Index 1 corresponds to BDay

# Place the party features in the correct columns (9th column from the end, excluding last 2)
input_data[0, -11:-4] = party_features[party]  # Excluding last 2, and counting 9 back

# Make the prediction when the button is pressed
if st.button('Predict GDP Growth'):
    # Make prediction using the model
    gdp_growth = model.predict(input_data)[0]

    # Look up President and VP from the dataset
    party_column = f"Party_{party}"

    # Ensure correct data type when comparing 'BDay' and the boolean value for party
    input_row = data[(data['BDay'] == bday) & (data[party_column] == True)]

    # Check if the filtered row has any matches
    if not input_row.empty:
        # Find the president by checking which president column is True
        #president_columns = input_row.filter(like="Name_").columns  # Filter columns starting with 'Name_'
        #president_name = president_columns[input_row[president_columns].values[0].argmax()].replace("Name_", "")
        
        # Find the Vice President by checking which VP column is True
        #vp_columns = input_row.filter(like="VP_").columns  # Filter columns starting with 'VP_'
        #vp_name = vp_columns[input_row[vp_columns].values[0].argmax()].replace("VP_", "")
        
        gdp_growth_percent = input_row.iloc[0, -2]  # Correct position for GDP Percent Growth

        # Display the results
        #st.write(f'Predicted GDP Growth: {gdp_growth}')
        st.write(f'Predicted GDP Growth Percent: {gdp_growth_percent * 100}%')
        #st.write(f'Predicted President: {president_name}')
        #st.write(f'Predicted Vice President: {vp_name}')
    else:
        st.write('No matching data found for the provided inputs.')
