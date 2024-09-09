import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
economic_data = pd.read_csv("C:/Users/dell/Documents/GitHub/the-a-team/scratch/Pres_nfo.csv")
personal_data = pd.read_csv('C:/Users/dell/Documents/GitHub/the-a-team/scratch/Historical Presidents Physical Data (More).csv')

# Merge the datasets on president names (First and Last Name in economic data)
merged_data = pd.merge(
    personal_data, 
    economic_data, 
    left_on=['name'], 
    right_on=['First Name'], 
    how='inner'
)

# Title of the app
st.title('Presidents Comparison: Economic Data & Personal Insights')

# Sidebar for President Selection
selected_presidents = st.sidebar.multiselect(
    "Select Presidents to Compare:",
    merged_data['name'].unique()
)

# Filter data based on selection
filtered_data = merged_data[merged_data['name'].isin(selected_presidents)]

# Display selected presidents' personal data
st.subheader('Selected Presidents: Personal Information')
st.dataframe(filtered_data[['name', 'height_in', 'weight_lb', 'corrected_iq']])

# Display GDP vs IQ scatter plot
st.subheader('IQ vs Nominal GDP')
fig, ax = plt.subplots()
ax.scatter(filtered_data['corrected_iq'], filtered_data['Nominal GDP (million of Dollars)'])
ax.set_xlabel('IQ')
ax.set_ylabel('Nominal GDP (millions)')
st.pyplot(fig)

# Display Inflation vs IQ scatter plot
st.subheader('IQ vs Inflation Rate')
fig, ax = plt.subplots()
ax.scatter(filtered_data['corrected_iq'], filtered_data['inflation rate'])
ax.set_xlabel('IQ')
ax.set_ylabel('Inflation Rate')
st.pyplot(fig)

# More charts for other economic indicators as needed...
