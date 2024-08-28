import plotly.express as px
import streamlit as st
import pandas as pd
import plotly as plt

# Load and clean data
@st.cache
def load_data():
    df = pd.read_csv('gdp_year_with_more.csv')
    df['GDP'] = df['GDP'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['Growth'] = df['Growth'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['inflation rate'] = df['inflation rate'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['Debt'] = df['Debt'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['Increase'] = df['Increase'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    return df

df = load_data()

def create_dashboard():
    selected_metric = st.selectbox("Select a Metric", df.columns[2:])
    chart = px.bar(df, x='President', y=selected_metric, color='President')
    st.plotly_chart(chart)

create_dashboard()

# Radar chart for selected presidents
def plot_radar_chart(president1, president2):
    metrics = ["GDP", "Growth", "inflation rate", "Debt", "Increase"]
    df_pres1 = df[df['President'] == president1][metrics].mean().values
    df_pres2 = df[df['President'] == president2][metrics].mean().values

    radar_data = pd.DataFrame({
        'Metric': metrics,
        president1: df_pres1,
        president2: df_pres2
    })

    fig = px.line_polar(radar_data, r='Metric', theta=metrics, line_close=True,
                        color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_traces(fill='toself')
    return fig

# Streamlit app setup
st.title("Presidential Economic Performance Comparison")
president1 = st.selectbox("Select the first President", options=df['President'].unique())
president2 = st.selectbox("Select the second President", options=df['President'].unique())

def plot_distribution():
    fig, ax = plt.subplots()
    sns.histplot(df['GDP'], kde=True, ax=ax)
    st.pyplot(fig)

plot_distribution()
