import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS for background image
page_bg_img = '''
<style>
body {
    background-image: url("C:/Users/dell/Documents/GitHub/the-a-team/Pres_pic/WH.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
'''

# Inject the custom CSS into the app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load the datasets
economic_data = pd.read_csv("C:/Users/dell/Documents/GitHub/the-a-team/scratch/Pres_nfo.csv")
personal_data = pd.read_csv('C:/Users/dell/Documents/GitHub/the-a-team/scratch/Historical Presidents Physical Data (More).csv')

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
    (1800, 2000)  # Default range
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

# --- FEATURE 1: Display President Images by Number (Only Once) ---
st.subheader('Selected Presidents with Images')

# Drop duplicate presidents based on 'full_name' and 'order'
unique_presidents_data = filtered_data[['full_name', 'order']].drop_duplicates()

# Display each president's image only once
for index, row in unique_presidents_data.iterrows():
    president_number = row['order']  # Assuming there’s an "order" column with the president’s number
    st.image(f'C:/Users/dell/Documents/GitHub/the-a-team/Pres_pic/{president_number}.jpg', caption=row['full_name'])

# --- FEATURE 2: Summary Statistics ---
st.subheader('Summary Statistics for Selected Presidents')
avg_iq = filtered_data['corrected_iq'].mean()
avg_gdp = filtered_data['Nominal GDP (million of Dollars)'].mean()  # Now this should work
avg_inflation = filtered_data['inflation rate'].mean()

st.write(f"**Average IQ**: {avg_iq:.2f}")
st.write(f"**Average Nominal GDP**: ${avg_gdp:,.2f} million")
st.write(f"**Average Inflation Rate**: {avg_inflation:.2f}%")

# --- FEATURE 3: Interactive Line Chart Option ---
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
        tooltip=['full_name', metric_x, metric_y]  # Tooltip feature
    ).interactive()
    st.altair_chart(line_chart, use_container_width=True)

# Additional charts or other economic indicators can be added as needed...
