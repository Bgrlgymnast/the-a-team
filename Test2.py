!pip install streamlit
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the datasets, eh? It's like cracking open a cold one, except with data.
df_presidents = pd.read_csv('presidentfinal_df.csv')
df_zodiac = pd.read_csv('zodiacs_df.csv')

# Gotta clean up those names, eh? We don't want any loose whitespace. Tidy like your toque.
df_presidents['President'] = df_presidents['First Name'].str.strip() + ' ' + df_presidents['Last Name'].str.strip()
df_zodiac['President'] = df_zodiac['President'].str.strip()

# Ok, now we check if any presidents are missing their zodiac sign, eh? Like when the beer's gone.
presidents_missing_zodiac = df_presidents[~df_presidents['President'].isin(df_zodiac['President'])]
st.write("Presidents without zodiac info:", presidents_missing_zodiac[['President']])

# Now we merge the datasets, kinda like putting the maple syrup on your pancakes.
df = pd.merge(df_presidents, df_zodiac, on='President', how='left')

# Just checking to make sure the merge worked, eh? We need to see the Presidents and their signs, like a puck and a stick.
st.write("Merged Data Preview:", df[['President', 'Sign']].head())

# Time to set up the categories for comparison, eh? You know, like GDP and Population... big numbers, eh?
category_mapping = {
    "Real GDP": "Real GDP (millions of 2017 dollars)",  # This is like the real dough they bring in, eh?
    "Population": "Population",  # How many hosers they got, eh?
    "Real GDP per Capita": "Real GDP per capita (year 2017 dollars)"  # How much each hoser is making, eh?
}

# Alright, let's get the sidebar going for president selection. It's like picking your favorite hockey player, eh?
st.sidebar.title("President Comparison")

# Multiselect for presidents, like choosing your team, eh?
selected_presidents = st.sidebar.multiselect(
    "Select Presidents", df['President'].unique())

# Now let's get some categories to compare, like comparing beers, eh? What do ya wanna see?
comparison_categories = st.sidebar.multiselect(
    "Select Categories", list(category_mapping.keys()))

# Now we gotta show the zodiac sign for the selected president. It's like checking what beer they like, eh?
selected_president = st.sidebar.selectbox("Select President for Horoscope", df['President'].unique())

# We're making sure the zodiac sign is found. If not, it's like saying "Sorry, eh? No sign for you."
if not df[df['President'] == selected_president].empty:
    zodiac_sign = df[df['President'] == selected_president]['Sign'].values[0]
    st.sidebar.markdown(f"**Zodiac Sign**: {zodiac_sign}")  # We show the zodiac sign, like "Hey look, he's a Pisces, eh?"
else:
    zodiac_sign = None
    st.sidebar.markdown(f"**Zodiac Sign**: Not Found")  # No sign? No problem. Still got beer, eh?

# Here's where we make up some horoscope predictions. Kinda like predicting the weather, eh? Just go with it.
horoscope_predictions = {
    "Aries": "Today is a great day for leadership, eh?",
    "Taurus": "Stability is key in decision-making today, eh?",
    "Gemini": "Communication will lead to big wins, like a hat-trick, eh?",
    "Cancer": "Focus on security and trust, like locking up your double-double, eh?",
    "Leo": "Now is the time for bold actions, like cracking open that 2-4, eh?",
    "Virgo": "Pay attention to details, like not spilling your beer, eh?",
    "Libra": "Harmony and balance will bring good things, like getting the last donut, eh?",
    "Scorpio": "Intense focus will help you get what you want, eh?",
    "Sagittarius": "Seek new adventures, like going for a rip, bud.",
    "Capricorn": "A methodical approach will win the day, like stacking wood for winter, eh?",
    "Aquarius": "Innovation will lead to breakthroughs, like inventing the hockey stick, eh?",
    "Pisces": "Go with your gut today, like knowing when to tap the keg, eh?"
}

# Now we show the horoscope prediction. If there's no sign, well, no horoscope for you, bud.
if zodiac_sign in horoscope_predictions:
    prediction = horoscope_predictions[zodiac_sign]
else:
    prediction = "No prediction available, eh?"

st.sidebar.markdown(f"**Horoscope Prediction**: {prediction}")

# Here's where the main show happens. You picked your presidents, now let's compare them, eh?
if selected_presidents and comparison_categories:
    st.title("Presidential Comparison")

    # We filter the data by the presidents you picked. Like picking your favorite hockey players, eh?
    df_filtered = df[df['President'].isin(selected_presidents)]

    # Now we make a graph for each category, like comparing goals in the hockey season, eh?
    for category in comparison_categories:
        column_name = category_mapping[category]  # Get the right column, eh?
        fig = px.line(df_filtered, x="Year", y=column_name, color="President", title=f"{category} Comparison")
        st.plotly_chart(fig)

st.sidebar.markdown("---")
st.sidebar.write("Make a prediction based on horoscope, eh?")
