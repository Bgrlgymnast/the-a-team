import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
economic_data = pd.read_csv('/mnt/data/Pres_nfo.csv')
personal_data = pd.read_csv('/mnt/data/Historical Presidents Physical Data (More).csv')

# Title of the app
st.title('Presidents Comparison: Economic Data & Personal Insights')

# Sidebar for President Selection
selected_presidents = st.sidebar.multiselect(
    "Select Presidents to Compare:",
    personal_data['name'].unique()
)

# Filter data based on selection
filtered_personal_data = personal_data[personal_data['name'].isin(selected_presidents)]
filtered_economic_data = economic_data[economic_data['First Name'].isin(filtered_personal_data['name'])]

# Display selected presidents' personal data
st.subheader('Selected Presidents: Personal Information')
st.dataframe(filtered_personal_data[['name', 'height_in', 'weight_lb', 'corrected_iq']])

# Display GDP vs IQ scatter plot
st.subheader('IQ vs Nominal GDP')
fig, ax = plt.subplots()
ax.scatter(filtered_personal_data['corrected_iq'], filtered_economic_data['Nominal GDP (million of Dollars)'])
ax.set_xlabel('IQ')
ax.set_ylabel('Nominal GDP (millions)')
st.pyplot(fig)

# Display Inflation vs IQ scatter plot
st.subheader('IQ vs Inflation Rate')
fig, ax = plt.subplots()
ax.scatter(filtered_personal_data['corrected_iq'], filtered_economic_data['inflation rate'])
ax.set_xlabel('IQ')
ax.set_ylabel('Inflation Rate')
st.pyplot(fig)

# More charts for other economic indicators as needed...

