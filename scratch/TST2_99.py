import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Custom CSS for background, fonts, and button styles
page_style = '''
<style>
body {
    background-image: url("Pres_pic/WH.jpg"); 
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    font-family: 'Roboto', sans-serif; /* Use a Google Font */
}

h1, h2, h3, h4 {
    color: #FFFFFF;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);  /* Text shadow for headers */
}

.stButton > button {
    background-color: #0044cc;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

.stButton > button:hover {
    background-color: #003399; /* Darker blue on hover */
}

.sidebar .sidebar-content {
    background-color: rgba(0, 0, 0, 0.8); /* Darken sidebar background */
    color: white;
}

img {
    transition: transform 0.2s ease-in-out, opacity 0.2s ease-in-out;  /* Smooth hover effect */
}

img:hover {
    transform: scale(1.05);  /* Slight zoom on hover */
    opacity: 0.8;            /* Fade on hover */
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

# Load the datasets (ensure paths are accessible or files are hosted)
economic_data = pd.read_csv("resources/Pres_nfo.csv")
personal_data = pd.read_csv('main/Historical President Physical Data (More).csv')

# Create a full name column in both datasets for proper matching
economic_data['full_name'] = economic_data['First Name'] + ' ' + economic_data['Last Name']
personal_data['full_name'] = personal_data['name']  # Assuming the name in personal data is full name

# Merge the datasets on full name
merged_data = pd.merge(
    personal_data, 
    economic_data, 
    left_on=['full_name'], 
    right_on=['full_name'], 
    how='inner'
)

# Clean the "Nominal GDP (million of Dollars)" column to ensure it is numeric
merged_data['Nominal GDP (million of Dollars)'] = pd.to_numeric(
    merged_data['Nominal GDP (million of Dollars)'].str.replace(',', ''), 
    errors='coerce'
)

# Ensure unique president names
unique_presidents = merged_data['full_name'].unique()

# Title of the app
st.title('Presidents Comparison: Economic Data & Personal Insights')

# Filter by Political Party
selected_party = st.sidebar.selectbox("Select Political Party:", merged_data['political_party'].unique())

# Filter presidents based on the selected party
filtered_party_data = merged_data[merged_data['political_party'] == selected_party]

# Filter by Term Year Range
year_range = st.sidebar.slider(
    "Select Presidential Term Year Range:",
    int(merged_data['term_begin_year'].min()),
    int(merged_data['term_end_year'].max()),
    (1800, 2024)  # Default range
)

# Filter presidents based on the selected year range and party
filtered_year_data = filtered_party_data[
    (filtered_party_data['term_begin_year'] >= year_range[0]) &
    (filtered_party_data['term_end_year'] <= year_range[1])
]

# Searchable dropdown with filtered presidents
selected_presidents = st.sidebar.multiselect(
    "Select Presidents to Compare:",
    filtered_year_data['full_name'].unique(),
    default=filtered_year_data['full_name'].unique()
)

# Filter data based on final selection
filtered_data = merged_data[merged_data['full_name'].isin(selected_presidents)]

# --- COLLAPSIBLE SECTIONS ---
with st.expander("Selected Presidents with Images"):
    # Drop duplicate presidents based on 'full_name' and 'order'
    unique_presidents_data = filtered_data[['full_name', 'order']].drop_duplicates()

    # Display each president's image only once
    for index, row in unique_presidents_data.iterrows():
        president_number = row['order']  # Assuming there’s an "order" column with the president’s number
        st.image(f'main/Pres_pic/{president_number}.jpg', caption=row['full_name'])

with st.expander("Summary Statistics for Selected Presidents"):
    avg_iq = filtered_data['corrected_iq'].mean()
    avg_gdp = filtered_data['Nominal GDP (million of Dollars)'].mean()  # Now this should work
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
    st.subheader(f'{metric_x.replace("_", " ").title()} vs {metric_y.replace("_", " ").title()}')
    fig, ax = plt.subplots()
    ax.scatter(filtered_data[metric_x], filtered_data[metric_y])
    ax.set_xlabel(metric_x.replace("_", " ").title())
    ax.set_ylabel(metric_y.replace("_", " ").title())
    st.pyplot(fig)

elif chart_type == 'Line Chart':
    st.subheader(f'{metric_x.replace("_", " ").title()} vs {metric_y.replace("_", " ").title()} (Line Chart)')
    line_chart = alt.Chart(filtered_data).mark_line().encode(
        x=metric_x,
        y=metric_y,
        tooltip=['full_name', metric_x, metric_y]  # Tooltip feature
    ).interactive()
    st.altair_chart(line_chart, use_container_width=True)
