import streamlit as st
import pandas as pd
import plotly.express as px

# Load the datasets
df_presidents = pd.read_csv('presidentfinal_df.csv')
df_zodiac = pd.read_csv('presidential_zodiac_sign.csv')

# Create a 'President' column by combining first and last name in the president dataset
df_presidents['President'] = df_presidents['First Name'] + ' ' + df_presidents['Last Name']

# Merge the datasets based on the president name
df = pd.merge(df_presidents, df_zodiac, on='President', how='left')

# Debugging: Show available columns to ensure proper merge
# st.write(df.head())  # Uncomment this to display the merged DataFrame for debugging

# Map categories to the actual column names
category_mapping = {
    "Real GDP": "Real GDP (millions of 2017 dollars)",
    "Population": "Population",
    "Real GDP per Capita": "Real GDP per capita (year 2017 dollars)"
}

# Sidebar for president selection
st.sidebar.title("President Comparison")

# Multiselect for presidents
selected_presidents = st.sidebar.multiselect(
    "Select Presidents", df['President'].unique())

# Multiselect for comparison categories
comparison_categories = st.sidebar.multiselect(
    "Select Categories", list(category_mapping.keys()))

# Display horoscope section
selected_president = st.sidebar.selectbox("Select President for Horoscope", df['President'].unique())

# Ensure Zodiac sign is correctly pulled from the merged DataFrame
zodiac_sign = df[df['President'] == selected_president]['Sign'].values[0]

# Check if the zodiac sign is properly retrieved for the selected president
st.sidebar.markdown(f"**Zodiac Sign**: {zodiac_sign}")

# Simple Horoscope prediction logic
horoscope_predictions = {
    "Aries": "Today is a great day for leadership.",
    "Taurus": "Stability is key in decision-making today.",
    "Gemini": "Communication will lead to significant achievements.",
    "Cancer": "Focus on security and trust.",
    "Leo": "Now is the time for bold actions and confidence.",
    "Virgo": "Pay attention to details and analytical skills today.",
    "Libra": "Harmony and balance will bring favorable outcomes.",
    "Scorpio": "Intense focus on transformation and control.",
    "Sagittarius": "Seek new horizons, great day for expanding ideas.",
    "Capricorn": "A methodical approach will win the day.",
    "Aquarius": "Innovation will lead to breakthroughs today.",
    "Pisces": "Intuition and empathy will guide you."
}

# Display the horoscope prediction
prediction = horoscope_predictions.get(zodiac_sign, "No prediction available.")
st.sidebar.markdown(f"**Horoscope Prediction**: {prediction}")

# Main section - Graph for comparison
if selected_presidents and comparison_categories:
    st.title("Presidential Comparison")

    # Filter the data based on selected presidents
    df_filtered = df[df['President'].isin(selected_presidents)]

    for category in comparison_categories:
        # Use the correct column name for the y-axis
        column_name = category_mapping[category]
        fig = px.line(df_filtered, x="Year", y=column_name, color="President", title=f"{category} Comparison")
        st.plotly_chart(fig)

st.sidebar.markdown("---")
st.sidebar.write("Make a prediction based on horoscope.")
