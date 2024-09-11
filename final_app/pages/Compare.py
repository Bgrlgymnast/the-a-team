import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import os

# Custom CSS for background, fonts, and button styles
page_style = '''
<style>
body {
    background-image: url("/Pres_pic/WH.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    font-family: 'Roboto', sans-serif;
}

h1, h2, h3, h4 {
    color: #FFFFFF;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
}

.stButton > button {
    background-color: #0044cc;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

.stButton > button:hover {
    background-color: #003399;
}

.stSidebar {
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
}

img {
    transition: transform 0.2s ease-in-out, opacity 0.2s ease-in-out;
}

img:hover {
    transform: scale(1.05);
    opacity: 0.8;
}
</style>
'''

# Inject the custom CSS into the app
st.markdown(page_style, unsafe_allow_html=True)

# --- THEME SELECTION ---
theme = st.sidebar.selectbox("Choose Theme", ["Default", "Dark", "Light"])

# Adjust theme based on selection
if theme == "Dark":
    st.markdown("<style>body { color: #ffffff; background-color: #121212; }</style>", unsafe_allow_html=True)
elif theme == "Light":
    st.markdown("<style>body { color: #000000; background-color: #f4f4f4; }</style>", unsafe_allow_html=True)

# Load the datasets
current_dir = os.getcwd()
if "final_app" not in current_dir and "scratch" not in current_dir:
    root_dir = str(current_dir)
    app_dir = os.path.join(root_dir, "final_app")
    scratch_dir = os.path.join(root_dir, "scratch")
elif "final_app" in current_dir:
    app_dir = str(current_dir)
    root_dir = os.path.dirname(current_dir)
    scratch_dir = os.path.join(root_dir, "scratch")
elif "scratch" in current_dir:
    scratch_dir = str(current_dir)
    root_dir = os.path.dirname(current_dir)
    app_dir = os.path.join(root_dir, "app")
economic_data = pd.read_csv(os.path.join(scratch_dir, "Pres_nfo.csv"))
personal_data = pd.read_csv(os.path.join(scratch_dir, "Historical Presidents Physical Data (More).csv"))

# Merge the datasets on 'order'
merged_data = pd.merge(
    personal_data, 
    economic_data, 
    left_on='order', 
    right_on='order', 
    how='outer'
)

# Clean the "Nominal GDP (million of Dollars)" column to ensure it is numeric
merged_data['Nominal GDP (million of Dollars)'] = pd.to_numeric(
    merged_data['Nominal GDP (million of Dollars)'].str.replace(',', ''), 
    errors='coerce'
)

# Clean the "Real GDP (millions of 2017 dollars)" column to ensure it is numeric
merged_data['Real GDP (millions of 2017 dollars)'] = pd.to_numeric(
    merged_data['Real GDP (millions of 2017 dollars)'].str.replace(',', ''), 
    errors='coerce'
)

# Ensure unique president names
unique_presidents = merged_data['name'].unique()

# Title of the app
st.title('Presidents Comparison: Economic Data & Personal Insights')

# --- ADVANCED FILTERING ---
# Allow multiple political party selections
selected_parties = st.sidebar.multiselect("Select Political Parties:", merged_data['political_party'].unique(), default=merged_data['political_party'].unique())

# Filter presidents based on the selected parties
filtered_party_data = merged_data[merged_data['political_party'].isin(selected_parties)]

# Filter by Term Year Range
year_range = st.sidebar.slider(
    "Select Presidential Term Year Range:",
    int(merged_data['term_begin_year'].min()),
    int(merged_data['term_end_year'].max()),
    (1789, 2024)  # Cover full range of presidents
)

# Filter presidents based on the selected year range and party
filtered_year_data = filtered_party_data[
    (filtered_party_data['term_begin_year'] >= year_range[0]) &
    (filtered_party_data['term_end_year'] <= year_range[1])
]

# Searchable dropdown with filtered presidents
selected_presidents = st.sidebar.multiselect(
    "Select Presidents to Compare:",
    filtered_year_data['name'].unique(),
    default=filtered_year_data['name'].unique()
)

# Filter data based on final selection
filtered_data = merged_data[merged_data['name'].isin(selected_presidents)]

# --- COLLAPSIBLE SECTIONS FOR PRESIDENT DETAILS ---
st.subheader('Selected Presidents with Detailed Information')
unique_presidents_data = filtered_data[['name', 'order']].drop_duplicates()

for index, row in unique_presidents_data.iterrows():
    president_number = row['order']

    image_path = os.path.join(app_dir, 'Pres_pic', f'{president_number}.jpg')

    # Check if the image exists, otherwise use a placeholder
    if not os.path.exists(image_path):
        image_path = os.path.join(app_dir, 'Pres_pic', '1.jpg')  # Fallback image if the specific one isn't found
    
    with st.expander(f"{row['name']} (Click for more info)"):
        st.image(image_path, caption=row['name'])
        # Display detailed information
        president_data = filtered_data[filtered_data['order'] == president_number].iloc[0]
        st.write(f"Term: {president_data['term_begin_year']} - {president_data['term_end_year']}")
        st.write(f"Party: {president_data['political_party']}")
        st.write(f"IQ: {president_data['corrected_iq']}")
        st.write(f"Height: {president_data['height_in']} inches")
        st.write(f"Weight: {president_data['weight_lb']} lbs")
        st.write(f"Nominal GDP: ${president_data['Nominal GDP (million of Dollars)']:,.2f} million")
        st.write(f"Real GDP: ${president_data['Real GDP (millions of 2017 dollars)']:,.2f} million")
        st.write(f"Inflation Rate: {president_data['inflation rate']}%")

# --- DATA VISUALIZATIONS ---
st.subheader("Political Party Breakdown")
party_chart = alt.Chart(merged_data).mark_bar().encode(
    x='political_party',
    y='count()',
    color='political_party'
).interactive()

st.altair_chart(party_chart, use_container_width=True)

# --- SUMMARY STATISTICS ---
with st.expander("Summary Statistics for Selected Presidents"):
    avg_iq = filtered_data['corrected_iq'].mean()
    avg_gdp = filtered_data['Nominal GDP (million of Dollars)'].mean()
    avg_inflation = filtered_data['inflation rate'].mean()

    st.write(f"**Average IQ**: {avg_iq:.2f}")
    st.write(f"**Average Nominal GDP**: ${avg_gdp:,.2f} million")
    st.write(f"**Average Inflation Rate**: {avg_inflation:.2f}%")

# --- PROGRESS BAR ---
st.subheader('Generating Data Insights...')
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)

# --- DOWNLOADABLE DATA ---
st.subheader("Download the filtered data")
csv = filtered_data.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name='filtered_presidents_data.csv', mime='text/csv')

# --- INTERACTIVE LINE CHART OPTION ---
st.subheader('Choose Metrics and Chart Type to Compare')

# User selects metrics and chart type (line or scatter)
metric_x = st.selectbox("Choose X-Axis Metric", ["corrected_iq", "height_in", "weight_lb"])
metric_y = st.selectbox("Choose Y-Axis Metric", ["Nominal GDP (million of Dollars)", "inflation rate", "Real GDP (millions of 2017 dollars)"])
chart_type = st.radio("Choose Chart Type", ['Scatter Plot', 'Line Chart'])

# Display Chart based on user selection
if chart_type == 'Scatter Plot':
    st.subheader(f'{metric_x} vs {metric_y}')
    fig, ax = plt.subplots()
    ax.scatter(filtered_data[metric_x], filtered_data[metric_y])
    ax.set_xlabel(metric_x.replace("_", " ").title())
    ax.set_ylabel(metric_y.replace("_", " ").title())
    st.pyplot(fig)

elif chart_type == 'Line Chart':
    st.subheader(f'{metric_x} vs {metric_y} (Line Chart)')
    line_chart = alt.Chart(filtered_data).mark_line().encode(
        x=metric_x,
        y=metric_y,
        tooltip=['name', metric_x, metric_y]
    ).interactive()
    st.altair_chart(line_chart, use_container_width=True)
