import streamlit as st
import pandas as pd
import altair as alt

# Step 1: Load the data and clean it
@st.cache
def load_data():
    df = pd.read_csv('gdp_year_with_more.csv')

    # Remove commas and dollar signs, then convert to numeric
    df['GDP'] = df['GDP'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['Growth'] = df['Growth'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['inflation rate'] = df['inflation rate'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['Debt'] = df['Debt'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['Increase'] = df['Increase'].replace({'\$': '', ',': ''}, regex=True).astype(float)

    return df

df = load_data()

# Step 2: Streamlit App Setup
st.title("Presidential Economic Performance Comparison")
st.write("""
    Select two U.S. Presidents to compare their economic performance based on:
    - GDP Growth
    - Growth
    - Inflation Rate
    - Debt
    - Increase
""")

# Step 3: President Selection
presidents = df['President'].unique()
president1 = st.selectbox("Select the first President", options=presidents)
president2 = st.selectbox("Select the second President", options=presidents)

# Step 4: Filter Data
df_pres1 = df[df['President'] == president1]
df_pres2 = df[df['President'] == president2]

# Step 5: Create comparison data
comparison_data = {
    "Metric": ["GDP", "Growth", "Inflation Rate", "Debt", "Increase"],
    president1: [
        df_pres1['GDP'].mean(),
        df_pres1['Growth'].mean(),
        df_pres1['inflation rate'].mean(),
        df_pres1['Debt'].mean(),
        df_pres1['Increase'].mean()
    ],
    president2: [
        df_pres2['GDP'].mean(),
        df_pres2['Growth'].mean(),
        df_pres2['inflation rate'].mean(),
        df_pres2['Debt'].mean(),
        df_pres2['Increase'].mean()
    ]
}

comparison_df = pd.DataFrame(comparison_data)

# Step 6: Display comparison graph
st.header(f"Comparison between {president1} and {president2}")
comparison_chart = alt.Chart(comparison_df).transform_fold(
    [president1, president2],
    as_=['President', 'Value']
).mark_bar().encode(
    x=alt.X('Metric:N', axis=alt.Axis(title='Metric')),
    y=alt.Y('Value:Q', axis=alt.Axis(title='Value')),
    color='President:N',
    column='Metric:N'
).properties(
    width=200,
    height=400
)

st.altair_chart(comparison_chart, use_container_width=True)

# Step 7: Show raw data if needed
st.subheader("Raw Data")
st.write("Data for comparison:", comparison_df)
