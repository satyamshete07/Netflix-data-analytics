import streamlit as st
import pandas as pd
import plotly.express as px
import os

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "..", "Dataset", "netflix_titles.csv")
# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Netflix Interactive Dashboard",
    layout="wide",
    page_icon="🎬"
)

# -------------------- NETFLIX UI --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #0b0b0b, #141414);
    color: white;
}
.title {
    text-align: center;
    font-size: 48px;
    color: #E50914;
    font-weight: bold;
}
.search-box {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOAD DATA --------------------
df = pd.read_csv(file_path)

df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year

# -------------------- SIDEBAR --------------------
st.sidebar.title("🎛️ Filters")

type_filter = st.sidebar.multiselect(
    "Type", df['type'].unique(), default=df['type'].unique()
)

country_filter = st.sidebar.multiselect(
    "Country", df['country'].dropna().unique()
)

year_filter = st.sidebar.slider(
    "Release Year",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    (2000, 2021)
)

# -------------------- HEADER --------------------
st.markdown('<div class="title">NETFLIX INTERACTIVE DASHBOARD</div>', unsafe_allow_html=True)

# -------------------- 🔍 SEARCH BAR --------------------
search = st.text_input("🔍 Search Netflix Titles", placeholder="Type a movie or show name...")

st.markdown("---")

# -------------------- FILTER DATA --------------------
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['release_year'].between(year_filter[0], year_filter[1]))
]

if country_filter:
    filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]

# ✅ APPLY SEARCH FILTER (IMPORTANT)
if search:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search, case=False, na=False)
    ]

# -------------------- KPI --------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Movies", filtered_df[filtered_df['type']=='Movie'].shape[0])
col2.metric("TV Shows", filtered_df[filtered_df['type']=='TV Show'].shape[0])
col3.metric("Countries", filtered_df['country'].nunique())
col4.metric("Total Titles", filtered_df.shape[0])

# -------------------- CHART 1 --------------------
fig1 = px.bar(
    filtered_df['type'].value_counts().reset_index(),
    x='count',
    y='type',
    orientation='h',
    title="Content Type Distribution",
    color='type',
    color_discrete_sequence=["#E50914", "#ffffff"]
)

# -------------------- CHART 2 --------------------
year_data = filtered_df['year_added'].value_counts().sort_index().reset_index()
year_data.columns = ['Year', 'Count']

fig2 = px.line(
    year_data,
    x='Year',
    y='Count',
    markers=True,
    title="Netflix Growth Over Time"
)

# -------------------- CHART 3 --------------------
top_countries = filtered_df['country'].value_counts().head(10).reset_index()
top_countries.columns = ['Country', 'Count']

fig3 = px.bar(
    top_countries,
    x='Count',
    y='Country',
    orientation='h',
    color='Count',
    color_continuous_scale='Reds',
    title="Top Countries"
)

# -------------------- CHART 4 --------------------
rating_data = filtered_df['rating'].value_counts().reset_index()
rating_data.columns = ['Rating', 'Count']

fig4 = px.pie(
    rating_data,
    names='Rating',
    values='Count',
    title="Content Ratings Distribution",
    color_discrete_sequence=px.colors.sequential.Reds
)

# -------------------- CHART 5 --------------------
genre_df = filtered_df.copy()
genre_df['listed_in'] = genre_df['listed_in'].str.split(', ')
genre_df = genre_df.explode('listed_in')

top_genres = genre_df['listed_in'].value_counts().head(10).reset_index()
top_genres.columns = ['Genre', 'Count']

fig5 = px.bar(
    top_genres,
    x='Count',
    y='Genre',
    orientation='h',
    color='Count',
    color_continuous_scale='Reds',
    title="Top Genres"
)

# -------------------- DISPLAY --------------------
col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)
col1.plotly_chart(fig3, use_container_width=True)
col2.plotly_chart(fig4, use_container_width=True)

st.plotly_chart(fig5, use_container_width=True)

# -------------------- DATA --------------------
st.markdown("## 📄 Data Explorer")
st.dataframe(filtered_df, use_container_width=True)