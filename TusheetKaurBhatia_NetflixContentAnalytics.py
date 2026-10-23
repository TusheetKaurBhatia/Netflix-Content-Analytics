"""
=============================================================================
 Netflix Content Analytics Dashboard
 Single-File Architecture: Backend, Data Cleaning, Analytics & Streamlit UI
 IBM Data Analytics Capstone Project
=============================================================================
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Netflix Content Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Netflix Cinematic Dark Theme
st.markdown("""
<style>
    /* Main container background */
    .stApp {
        background-color: #111111;
        color: #E5E5E5;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Header branding */
    .brand-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #E50914;
        letter-spacing: -0.5px;
        margin-bottom: 0px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-subtitle {
        color: #999999;
        font-size: 1.0rem;
        margin-top: -6px;
        margin-bottom: 24px;
        font-weight: 400;
    }
    
    /* KPI Card styling */
    .kpi-card {
        background: linear-gradient(135deg, #1d1d1d 0%, #171717 100%);
        border: 1px solid #2d2d2d;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: left;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #E50914;
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background-color: #E50914;
    }
    .kpi-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #A3A3A3;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.2;
    }
    .kpi-subtext {
        font-size: 0.78rem;
        color: #737373;
        margin-top: 4px;
    }
    
    /* Custom tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #181818;
        padding: 6px 10px;
        border-radius: 8px;
        border: 1px solid #262626;
    }
    .stTabs [data-baseweb="tab"] {
        color: #B3B3B3;
        font-weight: 600;
        font-size: 0.95rem;
        border-radius: 6px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E50914 !important;
        color: #FFFFFF !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #141414;
        border-right: 1px solid #262626;
    }
    
    /* Plot container card wrapper */
    .chart-container {
        background-color: #181818;
        border: 1px solid #262626;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 20px;
    }
    
    /* Tag / Badge */
    .badge-movie {
        background-color: #E50914;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-tv {
        background-color: #00D2D2;
        color: black;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-rating {
        background-color: #333333;
        color: #FFC107;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. DATA LOADING, CLEANING & PREPROCESSING PIPELINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_clean_data():
    """
    Loads raw netflix_titles.csv or cached cleaned dataset.
    Performs comprehensive sanitization:
      - Fixes misaligned duration values in rating column (e.g. Louis C.K. specials)
      - Imputes missing directors, cast, country, date_added, and rating
      - Normalizes dates, extracts year_added, month_added
      - Parses numeric durations (minutes for movies, seasons for TV shows)
      - Classifies target audience maturity tiers
      - Calculates content acquisition lag (year_added - release_year)
    """
    cleaned_file_path = "cleaned_netflix_titles.csv"
    raw_subfolder_path = os.path.join("netflix_titles.csv", "netflix_titles.csv")
    raw_root_path = "netflix_titles.csv"
    
    if os.path.exists(cleaned_file_path):
        df = pd.read_csv(cleaned_file_path)
        # Ensure correct datatypes
        df["release_year"] = df["release_year"].astype(int)
        df["year_added"] = df["year_added"].astype(int)
        df["duration_value"] = pd.to_numeric(df["duration_value"], errors="coerce").fillna(0).astype(int)
        return df

    # Fallback to load and clean raw CSV if cleaned file is missing
    target_raw = raw_subfolder_path if os.path.exists(raw_subfolder_path) else raw_root_path
    if not os.path.exists(target_raw):
        st.error(f"Cannot find dataset at {raw_subfolder_path} or {raw_root_path}.")
        st.stop()
        
    df = pd.read_csv(target_raw)

    # Step 1: Fix misaligned rating/duration entries
    shift_mask = df["rating"].str.contains("min|Season", na=False)
    for idx in df[shift_mask].index:
        df.loc[idx, "duration"] = df.loc[idx, "rating"]
        df.loc[idx, "rating"] = "TV-MA"

    # Step 2: Impute missing values
    df["rating"] = df["rating"].fillna("UR").replace("", "UR")
    df["director"] = df["director"].fillna("Unknown").replace("", "Unknown")
    df["cast"] = df["cast"].fillna("Unknown").replace("", "Unknown")
    df["country"] = df["country"].fillna("Unknown").replace("", "Unknown")

    # Step 3: Extract primary country
    df["primary_country"] = df["country"].apply(
        lambda x: x.split(",")[0].strip() if x != "Unknown" else "Unknown"
    )

    # Step 4: Parse dates & impute missing dates
    df["date_added_clean"] = pd.to_datetime(df["date_added"].astype(str).str.strip(), errors="coerce")
    missing_dates = df["date_added_clean"].isna()
    df.loc[missing_dates, "date_added_clean"] = pd.to_datetime(
        df.loc[missing_dates, "release_year"].astype(str) + "-01-01"
    )
    df["year_added"] = df["date_added_clean"].dt.year.astype(int)
    df["month_added"] = df["date_added_clean"].dt.month_name()
    df["date_added"] = df["date_added_clean"].dt.strftime("%B %d, %Y")
    df = df.drop(columns=["date_added_clean"])

    # Step 5: Parse duration into numeric value & unit
    def parse_dur(row):
        s = str(row["duration"]).strip()
        if "min" in s:
            try:
                return int(s.replace("min", "").strip()), "min"
            except:
                return 0, "min"
        elif "Season" in s:
            try:
                return int(s.split(" ")[0].strip()), "Season(s)"
            except:
                return 0, "Season(s)"
        return 0, "Unknown"

    parsed = df.apply(parse_dur, axis=1)
    df["duration_value"] = [p[0] for p in parsed]
    df["duration_unit"] = [p[1] for p in parsed]

    # Step 6: Map Audience Maturity Groups
    audience_map = {
        "TV-MA": "Adults (18+)",
        "R": "Adults (18+)",
        "NC-17": "Adults (18+)",
        "TV-14": "Teens (14+)",
        "PG-13": "Teens (14+)",
        "TV-PG": "Older Kids (7+)",
        "PG": "Older Kids (7+)",
        "TV-Y7": "Older Kids (7+)",
        "TV-Y7-FV": "Older Kids (7+)",
        "TV-Y": "Kids (All)",
        "TV-G": "Kids (All)",
        "G": "Kids (All)",
        "NR": "Unrated / Other",
        "UR": "Unrated / Other",
    }
    df["target_audience"] = df["rating"].map(audience_map).fillna("Unrated / Other")

    # Step 7: Primary genre & acquisition lag
    df["primary_genre"] = df["listed_in"].apply(lambda x: x.split(",")[0].strip() if pd.notna(x) else "Unknown")
    df["acquisition_lag"] = df["year_added"] - df["release_year"]
    df["acquisition_lag"] = df["acquisition_lag"].apply(lambda x: max(x, 0))

    return df


df_master = load_and_clean_data()

# Helper color definitions
NETFLIX_RED = "#E50914"
NETFLIX_DARK = "#141414"
NETFLIX_CARD = "#1f1f1f"
PALETTE = ["#E50914", "#00D2D2", "#F5C518", "#8B5CF6", "#FF6B6B", "#48BB78", "#ED8936", "#CBD5E0"]

def get_plot_layout():
    """Returns standardized dark layout for Plotly visuals."""
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E5E5", family="Helvetica Neue, sans-serif"),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(font=dict(color="#CCCCCC")),
        hoverlabel=dict(bgcolor="#222222", font_size=13, font_color="#FFFFFF"),
    )


# -----------------------------------------------------------------------------
# 3. INTERACTIVE SIDEBAR FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#E50914; font-weight:800; letter-spacing:1px;'>NETFLIX FILTERS</h2>", unsafe_allow_html=True)
    st.caption("Customize dashboard views and analytics in real time.")
    st.markdown("---")

    # Filter 1: Search Query
    search_query = st.text_input("🔍 Search Catalog", placeholder="Title, Director, Cast...").strip()

    # Filter 2: Content Type
    type_options = ["All Types"] + sorted(df_master["type"].unique().tolist())
    selected_type = st.radio("Content Format", type_options, index=0, horizontal=True)

    # Filter 3: Year Added Range
    min_add_yr = int(df_master["year_added"].min())
    max_add_yr = int(df_master["year_added"].max())
    selected_add_range = st.slider(
        "📅 Year Added to Netflix",
        min_value=min_add_yr,
        max_value=max_add_yr,
        value=(min_add_yr, max_add_yr)
    )

    # Filter 4: Release Year Range
    min_rel_yr = int(df_master["release_year"].min())
    max_rel_yr = int(df_master["release_year"].max())
    selected_rel_range = st.slider(
        "🎞️ Content Release Year",
        min_value=min_rel_yr,
        max_value=max_rel_yr,
        value=(min_rel_yr, max_rel_yr)
    )

    # Filter 5: Target Audience Maturity
    all_audiences = sorted(df_master["target_audience"].unique().tolist())
    selected_audiences = st.multiselect("🎯 Target Audience", all_audiences, default=all_audiences)

    # Filter 6: Genres (exploded selection)
    all_genres = sorted(list(set(g.strip() for sublist in df_master["listed_in"].dropna().str.split(",") for g in sublist)))
    selected_genres = st.multiselect("🎭 Filter by Genres", all_genres, default=[])

    # Filter 7: Countries (exploded selection)
    all_countries = sorted(list(set(c.strip() for sublist in df_master["country"].dropna().str.split(",") for c in sublist if c.strip() and c.strip() != "Unknown")))
    selected_countries = st.multiselect("🌍 Filter by Countries", all_countries, default=[])

    st.markdown("---")
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()


# -----------------------------------------------------------------------------
# 4. FILTER EXECUTION ENGINE
# -----------------------------------------------------------------------------
df_filtered = df_master.copy()

# Apply Content Type
if selected_type != "All Types":
    df_filtered = df_filtered[df_filtered["type"] == selected_type]

# Apply Year Ranges
df_filtered = df_filtered[
    (df_filtered["year_added"] >= selected_add_range[0]) &
    (df_filtered["year_added"] <= selected_add_range[1]) &
    (df_filtered["release_year"] >= selected_rel_range[0]) &
    (df_filtered["release_year"] <= selected_rel_range[1])
]

# Apply Audience
if selected_audiences:
    df_filtered = df_filtered[df_filtered["target_audience"].isin(selected_audiences)]

# Apply Genre Filter
if selected_genres:
    pattern = "|".join([f"(?:^|,\\s*){g}(?:\\s*,|$)" for g in selected_genres])
    df_filtered = df_filtered[df_filtered["listed_in"].str.contains(pattern, na=False, regex=True)]

# Apply Country Filter
if selected_countries:
    pattern_c = "|".join([f"(?:^|,\\s*){c}(?:\\s*,|$)" for c in selected_countries])
    df_filtered = df_filtered[df_filtered["country"].str.contains(pattern_c, na=False, regex=True)]

# Apply Search Query
if search_query:
    q = search_query.lower()
    df_filtered = df_filtered[
        df_filtered["title"].str.lower().str.contains(q, na=False) |
        df_filtered["director"].str.lower().str.contains(q, na=False) |
        df_filtered["cast"].str.lower().str.contains(q, na=False) |
        df_filtered["description"].str.lower().str.contains(q, na=False)
    ]


# -----------------------------------------------------------------------------
# 5. DASHBOARD HEADER & EXECUTIVE KPI SCORECARD
# -----------------------------------------------------------------------------
st.markdown("""
<div class="brand-title">
    <span>🎬 NETFLIX</span> CONTENT ANALYTICS
</div>
<div class="brand-subtitle">
    Executive catalog intelligence, global content expansion, audience demographics, and category trends
</div>
""", unsafe_allow_html=True)

# Calculate Key Performance Indicators
total_titles = len(df_filtered)
movie_count = len(df_filtered[df_filtered["type"] == "Movie"])
tv_count = len(df_filtered[df_filtered["type"] == "TV Show"])
movie_pct = (movie_count / total_titles * 100) if total_titles > 0 else 0
tv_pct = (tv_count / total_titles * 100) if total_titles > 0 else 0

# Count unique countries & genres in filtered slice
filtered_countries = set(c.strip() for sublist in df_filtered["country"].dropna().str.split(",") for c in sublist if c.strip() and c.strip() != "Unknown")
filtered_genres = set(g.strip() for sublist in df_filtered["listed_in"].dropna().str.split(",") for g in sublist if g.strip())

# Mature content share (TV-MA + R)
mature_count = len(df_filtered[df_filtered["rating"].isin(["TV-MA", "R", "NC-17"])])
mature_pct = (mature_count / total_titles * 100) if total_titles > 0 else 0

# Median Movie Runtime
movies_filtered = df_filtered[df_filtered["type"] == "Movie"]
median_runtime = int(movies_filtered["duration_value"].median()) if len(movies_filtered) > 0 else 0

# Render KPI Columns
kpi_cols = st.columns(6)

with kpi_cols[0]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Catalog Volume</div>
        <div class="kpi-value">{total_titles:,}</div>
        <div class="kpi-subtext">Titles currently matched</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[1]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Movies vs TV</div>
        <div class="kpi-value">{movie_pct:.0f}% <span style='font-size:1.0rem; color:#A3A3A3;'>/ {tv_pct:.0f}%</span></div>
        <div class="kpi-subtext">{movie_count:,} Films | {tv_count:,} Series</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[2]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Global Footprint</div>
        <div class="kpi-value">{len(filtered_countries)}</div>
        <div class="kpi-subtext">Producing nations active</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[3]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Genre Breadth</div>
        <div class="kpi-value">{len(filtered_genres)}</div>
        <div class="kpi-subtext">Entertainment verticals</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[4]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Maturity Skew</div>
        <div class="kpi-value">{mature_pct:.1f}%</div>
        <div class="kpi-subtext">Adults (TV-MA / R rated)</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[5]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Avg Film Runtime</div>
        <div class="kpi-value">{median_runtime} <span style='font-size:1.0rem; color:#A3A3A3;'>min</span></div>
        <div class="kpi-subtext">Median movie length</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. FIVE ANALYTICS MODULES (TABBED INTERFACE)
# -----------------------------------------------------------------------------
tab_growth, tab_genre, tab_geo, tab_ratings, tab_explorer = st.tabs([
    "📈 Content Growth & Trends",
    "🎭 Genre & Vertical Analysis",
    "🌍 Global Production Footprint",
    "🎯 Ratings & Runtime Specs",
    "🔍 Content Explorer & Search"
])

# -----------------------------------------------------------------------------
# MODULE 1: CONTENT GROWTH & TIMELINE TRENDS
# -----------------------------------------------------------------------------
with tab_growth:
    st.subheader("Catalog Expansion & Acquisition Dynamics")
    
    col_g1, col_g2 = st.columns([1.6, 1])

    with col_g1:
        # Annual additions split by format
        additions = df_filtered.groupby(["year_added", "type"]).size().reset_index(name="count")
        fig_add = px.area(
            additions,
            x="year_added",
            y="count",
            color="type",
            title="Annual Content Additions by Format (Movies vs TV Shows)",
            color_discrete_map={"Movie": NETFLIX_RED, "TV Show": "#00D2D2"},
            labels={"year_added": "Year Added to Platform", "count": "Titles Added", "type": "Format"}
        )
        fig_add.update_layout(get_plot_layout())
        fig_add.update_xaxes(showgrid=True, gridcolor="#262626")
        fig_add.update_yaxes(showgrid=True, gridcolor="#262626")
        st.plotly_chart(fig_add, use_container_width=True)

    with col_g2:
        # Acquisition Lag Distribution (Fresh Originals vs Catalog Archives)
        lag_bins = pd.cut(
            df_filtered["acquisition_lag"],
            bins=[-1, 0, 2, 5, 10, 100],
            labels=["Day-1 / Originals (0 yr)", "Recent (1-2 yrs)", "Mid Catalog (3-5 yrs)", "Older (6-10 yrs)", "Archive (10+ yrs)"]
        ).value_counts().reset_index()
        lag_bins.columns = ["Lag Category", "Count"]

        fig_lag = px.bar(
            lag_bins,
            x="Count",
            y="Lag Category",
            orientation="h",
            title="Acquisition Lag (Release Year to Netflix Addition)",
            color="Count",
            color_continuous_scale=["#333333", NETFLIX_RED],
        )
        fig_lag.update_layout(get_plot_layout(), coloraxis_showscale=False)
        fig_lag.update_xaxes(showgrid=True, gridcolor="#262626")
        st.plotly_chart(fig_lag, use_container_width=True)

    # Monthly Seasonality Drop Heatmap
    st.markdown("#### Monthly Content Release Density")
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    monthly_data = df_filtered.groupby(["month_added", "type"]).size().unstack(fill_value=0)
    monthly_data = monthly_data.reindex(month_order).fillna(0).reset_index()

    fig_season = go.Figure()
    fig_season.add_trace(go.Bar(
        x=monthly_data["month_added"],
        y=monthly_data["Movie"] if "Movie" in monthly_data else [0]*12,
        name="Movies",
        marker_color=NETFLIX_RED
    ))
    fig_season.add_trace(go.Bar(
        x=monthly_data["month_added"],
        y=monthly_data["TV Show"] if "TV Show" in monthly_data else [0]*12,
        name="TV Shows",
        marker_color="#00D2D2"
    ))
    fig_season.update_layout(
        barmode="stack",
        title="Content Ingestion Seasonality by Calendar Month",
        xaxis_title="Calendar Month",
        yaxis_title="Total Titles Ingested",
        **get_plot_layout()
    )
    fig_season.update_xaxes(showgrid=False)
    fig_season.update_yaxes(showgrid=True, gridcolor="#262626")
    st.plotly_chart(fig_season, use_container_width=True)


# -----------------------------------------------------------------------------
# MODULE 2: GENRE & CATEGORY ANALYSIS
# -----------------------------------------------------------------------------
with tab_genre:
    st.subheader("Genre Portfolio Breakdown & Dominance")

    col_gen1, col_gen2 = st.columns([1.4, 1])

    # Explode genres for accurate distribution
    genre_series = df_filtered["listed_in"].dropna().str.split(", ")
    exploded_genres = df_filtered[["type"]].join(genre_series.explode("listed_in"))
    exploded_genres = exploded_genres.rename(columns={"listed_in": "genre"})
    exploded_genres["genre"] = exploded_genres["genre"].str.strip()

    top_genres = exploded_genres["genre"].value_counts().head(15).index.tolist()
    genre_chart_data = exploded_genres[exploded_genres["genre"].isin(top_genres)]
    genre_grouped = genre_chart_data.groupby(["genre", "type"]).size().reset_index(name="count")

    with col_gen1:
        fig_genre = px.bar(
            genre_grouped,
            y="genre",
            x="count",
            color="type",
            orientation="h",
            title="Top 15 Categories by Catalog Volume",
            color_discrete_map={"Movie": NETFLIX_RED, "TV Show": "#00D2D2"},
            barmode="stack"
        )
        fig_genre.update_layout(
            yaxis={"categoryorder": "total ascending"},
            **get_plot_layout()
        )
        fig_genre.update_xaxes(showgrid=True, gridcolor="#262626")
        st.plotly_chart(fig_genre, use_container_width=True)

    with col_gen2:
        top_10_pie = exploded_genres["genre"].value_counts().head(8).reset_index()
        top_10_pie.columns = ["Genre", "Count"]
        fig_pie = px.pie(
            top_10_pie,
            names="Genre",
            values="Count",
            title="Share of Top 8 Entertainment Verticals",
            hole=0.45,
            color_discrete_sequence=PALETTE
        )
        fig_pie.update_layout(get_plot_layout())
        st.plotly_chart(fig_pie, use_container_width=True)

    # Genre Growth Over Time
    st.markdown("#### Genre Trajectory Over Recent Years")
    top_5_genres = exploded_genres["genre"].value_counts().head(5).index.tolist()
    
    genre_years = df_filtered[["year_added"]].join(genre_series.explode("listed_in"))
    genre_years = genre_years.rename(columns={"listed_in": "genre"})
    genre_years["genre"] = genre_years["genre"].str.strip()
    genre_years = genre_years[genre_years["genre"].isin(top_5_genres)]
    genre_trend = genre_years.groupby(["year_added", "genre"]).size().reset_index(name="count")
    genre_trend = genre_trend[genre_trend["year_added"] >= 2014]

    fig_trend = px.line(
        genre_trend,
        x="year_added",
        y="count",
        color="genre",
        title="Annual Growth of Top 5 Dominant Genres (2014 - 2021)",
        markers=True,
        color_discrete_sequence=PALETTE
    )
    fig_trend.update_layout(get_plot_layout())
    fig_trend.update_xaxes(showgrid=True, gridcolor="#262626")
    fig_trend.update_yaxes(showgrid=True, gridcolor="#262626")
    st.plotly_chart(fig_trend, use_container_width=True)


# -----------------------------------------------------------------------------
# MODULE 3: GLOBAL PRODUCTION & GEOGRAPHIC FOOTPRINT
# -----------------------------------------------------------------------------
with tab_geo:
    st.subheader("International Production Reach & Top Origin Markets")

    # Explode countries for accurate counts
    country_series = df_filtered["country"].dropna().str.split(", ")
    exploded_countries = df_filtered[["type"]].join(country_series.explode("country"))
    exploded_countries = exploded_countries.rename(columns={"country": "country_name"})
    exploded_countries["country_name"] = exploded_countries["country_name"].str.strip()
    exploded_countries = exploded_countries[exploded_countries["country_name"] != "Unknown"]

    country_counts = exploded_countries["country_name"].value_counts().reset_index()
    country_counts.columns = ["Country", "Total Titles"]

    # World Choropleth Map
    fig_map = px.choropleth(
        country_counts,
        locations="Country",
        locationmode="country names",
        color="Total Titles",
        hover_name="Country",
        title="Global Density of Netflix Titles Produced",
        color_continuous_scale=[[0, "#2b0a0d"], [0.2, "#800c14"], [0.6, "#c40b15"], [1.0, "#ff2e3a"]],
    )
    fig_map.update_geos(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#333333",
        bgcolor="rgba(0,0,0,0)",
        lakecolor="#111111",
        landcolor="#1c1c1c"
    )
    fig_map.update_layout(
        **get_plot_layout(),
        coloraxis_colorbar=dict(title="Titles", thickness=15, len=0.6)
    )
    st.plotly_chart(fig_map, use_container_width=True)

    col_c1, col_c2 = st.columns([1.5, 1])

    with col_c1:
        top_10_countries = country_counts.head(10)
        fig_c_bar = px.bar(
            top_10_countries,
            x="Total Titles",
            y="Country",
            orientation="h",
            title="Top 10 Content Producing Countries",
            color="Total Titles",
            color_continuous_scale=["#3d080b", NETFLIX_RED]
        )
        fig_c_bar.update_layout(
            yaxis={"categoryorder": "total ascending"},
            **get_plot_layout(),
            coloraxis_showscale=False
        )
        fig_c_bar.update_xaxes(showgrid=True, gridcolor="#262626")
        st.plotly_chart(fig_c_bar, use_container_width=True)

    with col_c2:
        # US vs International Ratio
        us_count = len(df_filtered[df_filtered["country"].str.contains("United States", na=False)])
        intl_count = total_titles - us_count
        origin_df = pd.DataFrame({
            "Origin": ["United States", "International / Rest of World"],
            "Count": [us_count, intl_count]
        })
        fig_origin = px.pie(
            origin_df,
            names="Origin",
            values="Count",
            title="Domestic (US) vs. International Titles",
            hole=0.5,
            color="Origin",
            color_discrete_map={"United States": NETFLIX_RED, "International / Rest of World": "#00D2D2"}
        )
        fig_origin.update_layout(get_plot_layout())
        st.plotly_chart(fig_origin, use_container_width=True)


# -----------------------------------------------------------------------------
# MODULE 4: AUDIENCE DEMOGRAPHICS & MATURITY RATINGS
# -----------------------------------------------------------------------------
with tab_ratings:
    st.subheader("Audience Segmentation, Ratings & Runtime Analytics")

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        # Target audience distribution
        aud_df = df_filtered["target_audience"].value_counts().reset_index()
        aud_df.columns = ["Target Audience", "Count"]
        fig_aud = px.pie(
            aud_df,
            names="Target Audience",
            values="Count",
            title="Target Audience Demographic Allocation",
            hole=0.45,
            color_discrete_sequence=["#E50914", "#F5C518", "#00D2D2", "#48BB78", "#8B5CF6"]
        )
        fig_aud.update_layout(get_plot_layout())
        st.plotly_chart(fig_aud, use_container_width=True)

    with col_r2:
        # Maturity Rating distribution by format
        top_ratings = df_filtered["rating"].value_counts().head(8).index.tolist()
        rating_sub = df_filtered[df_filtered["rating"].isin(top_ratings)]
        rating_grouped = rating_sub.groupby(["rating", "type"]).size().reset_index(name="Count")

        fig_rate = px.bar(
            rating_grouped,
            x="rating",
            y="Count",
            color="type",
            barmode="group",
            title="Maturity Rating Distribution by Content Format",
            color_discrete_map={"Movie": NETFLIX_RED, "TV Show": "#00D2D2"}
        )
        fig_rate.update_layout(get_plot_layout())
        fig_rate.update_xaxes(showgrid=False)
        fig_rate.update_yaxes(showgrid=True, gridcolor="#262626")
        st.plotly_chart(fig_rate, use_container_width=True)

    st.markdown("---")
    st.subheader("Runtime & Duration Distribution")

    col_dur1, col_dur2 = st.columns(2)

    with col_dur1:
        # Movie Runtime distribution
        movies_df = df_filtered[(df_filtered["type"] == "Movie") & (df_filtered["duration_value"] > 0)]
        fig_m_dur = px.histogram(
            movies_df,
            x="duration_value",
            nbins=40,
            title="Movie Length Distribution (in Minutes)",
            color_discrete_sequence=[NETFLIX_RED],
            labels={"duration_value": "Duration (Minutes)"}
        )
        fig_m_dur.update_layout(get_plot_layout(), bargap=0.08)
        fig_m_dur.update_xaxes(showgrid=True, gridcolor="#262626")
        fig_m_dur.update_yaxes(showgrid=True, gridcolor="#262626")
        st.plotly_chart(fig_m_dur, use_container_width=True)

    with col_dur2:
        # TV Show Season distribution
        tv_df = df_filtered[(df_filtered["type"] == "TV Show") & (df_filtered["duration_value"] > 0)]
        tv_seasons = tv_df["duration_value"].value_counts().reset_index()
        tv_seasons.columns = ["Seasons", "TV Shows"]
        tv_seasons = tv_seasons.sort_values(by="Seasons")

        fig_tv_dur = px.bar(
            tv_seasons,
            x="Seasons",
            y="TV Shows",
            title="TV Show Longevity (Number of Seasons)",
            color="TV Shows",
            color_continuous_scale=["#005757", "#00D2D2"]
        )
        fig_tv_dur.update_layout(get_plot_layout(), coloraxis_showscale=False)
        fig_tv_dur.update_xaxes(showgrid=False, dtick=1)
        fig_tv_dur.update_yaxes(showgrid=True, gridcolor="#262626")
        st.plotly_chart(fig_tv_dur, use_container_width=True)


# -----------------------------------------------------------------------------
# MODULE 5: SEARCHABLE CONTENT EXPLORER & DETAIL CARDS
# -----------------------------------------------------------------------------
with tab_explorer:
    st.subheader("Interactive Catalog Explorer & Title Inspector")
    st.caption("Inspect granular attributes, synopses, and production credits.")

    # Top search bar status
    st.write(f"Showing **{len(df_filtered):,}** records matching active criteria.")

    # Data Table View
    display_cols = ["show_id", "title", "type", "release_year", "rating", "target_audience", "duration", "primary_country", "listed_in"]
    st.dataframe(
        df_filtered[display_cols],
        column_config={
            "show_id": st.column_config.TextColumn("ID", width="small"),
            "title": st.column_config.TextColumn("Title", width="medium"),
            "type": st.column_config.TextColumn("Type", width="small"),
            "release_year": st.column_config.NumberColumn("Year", format="%d", width="small"),
            "rating": st.column_config.TextColumn("Rating", width="small"),
            "target_audience": st.column_config.TextColumn("Audience", width="medium"),
            "duration": st.column_config.TextColumn("Duration", width="small"),
            "primary_country": st.column_config.TextColumn("Country", width="medium"),
            "listed_in": st.column_config.TextColumn("Genres", width="large"),
        },
        use_container_width=True,
        hide_index=True,
        height=380
    )

    # Detailed Title Inspector Card
    st.markdown("#### 🎬 Select Title to View Details")
    if not df_filtered.empty:
        title_options = df_filtered["title"].tolist()
        selected_title = st.selectbox("Choose a title:", title_options, index=0)
        
        title_record = df_filtered[df_filtered["title"] == selected_title].iloc[0]

        type_badge = "badge-movie" if title_record["type"] == "Movie" else "badge-tv"

        st.markdown(f"""
        <div style="background-color: #1a1a1a; border: 1px solid #333333; border-radius: 10px; padding: 22px; margin-top: 10px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <h3 style="margin: 0; color: #FFFFFF; font-size: 1.5rem;">{title_record['title']}</h3>
                <span class="{type_badge}">{title_record['type']}</span>
                <span class="badge-rating">{title_record['rating']}</span>
                <span style="color: #999999; font-size: 0.9rem;">({title_record['release_year']})</span>
            </div>
            <p style="color: #cccccc; font-size: 0.95rem; line-height: 1.5; margin-bottom: 16px;">
                {title_record['description']}
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; font-size: 0.88rem;">
                <div><strong style="color: #E50914;">Director:</strong> <span style="color:#E5E5E5;">{title_record['director']}</span></div>
                <div><strong style="color: #E50914;">Country:</strong> <span style="color:#E5E5E5;">{title_record['country']}</span></div>
                <div><strong style="color: #E50914;">Duration:</strong> <span style="color:#E5E5E5;">{title_record['duration']}</span></div>
                <div><strong style="color: #E50914;">Date Added:</strong> <span style="color:#E5E5E5;">{title_record['date_added']}</span></div>
                <div><strong style="color: #E50914;">Genres:</strong> <span style="color:#E5E5E5;">{title_record['listed_in']}</span></div>
                <div><strong style="color: #E50914;">Acquisition Lag:</strong> <span style="color:#E5E5E5;">{title_record['acquisition_lag']} year(s)</span></div>
            </div>
            <div style="margin-top: 12px; font-size: 0.88rem;">
                <strong style="color: #E50914;">Key Cast:</strong> <span style="color: #BBBBBB;">{title_record['cast']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Download filtered data button
        st.markdown("<br>", unsafe_allow_html=True)
        csv_download = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_download,
            file_name="netflix_filtered_data.csv",
            mime="text/csv",
            use_container_width=False
        )
    else:
        st.info("No records match your active filter settings. Try broadening your criteria.")


# -----------------------------------------------------------------------------
# 7. DASHBOARD FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666666; font-size: 0.85rem; padding: 12px;">
    Netflix Content Analytics Dashboard | IBM Data Analytics Capstone | Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
