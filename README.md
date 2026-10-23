# 🎬 Netflix Content Analytics Dashboard

**Interactive Data Analytics Project | Python • Pandas • Streamlit • Plotly**

## 📌 Project Overview

The Netflix Content Analytics Dashboard is an interactive data analytics application developed to explore Netflix's movies and TV shows catalog.

The project uses data analysis and visualization techniques to identify patterns in content distribution, release years, genres, countries, maturity ratings, and content duration. The dashboard presents these findings through interactive charts, summary metrics, filters, and a searchable content explorer.

The main objective is to transform raw catalog data into meaningful insights through a simple and user-friendly interface.

## 🎯 Project Objectives

- Analyze the distribution of movies and TV shows.
- Explore content release trends and Netflix catalog addition patterns.
- Identify the most frequently listed genres.
- Analyze the geographical distribution of content.
- Examine maturity ratings and content duration.
- Provide interactive filters and title-level exploration.
- Present analytical findings using visualizations and summary metrics.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming and analytical logic |
| Pandas | Data cleaning, transformation, and analysis |
| Streamlit | Interactive web application |
| Plotly | Interactive charts and visualizations |
| CSV | Dataset format |

## 📊 Dashboard Modules

### 1. Key Performance Indicators
Displays important catalog metrics, including the total number of titles, movie and TV show distribution, country coverage, genre diversity, and runtime statistics.

### 2. Content Growth and Trend Analysis
Explores yearly content additions, release-year trends, monthly patterns, and the gap between a title's release date and its addition to Netflix.

### 3. Genre Analysis
Examines the distribution of genres and compares content categories using interactive charts.

### 4. Global Content Analysis
Explores country-wise content distribution and visualizes the geographical footprint of titles in the dataset.

### 5. Ratings and Duration Analysis
Analyzes maturity ratings, movie runtimes, and TV show season counts.

### 6. Content Explorer
Provides a searchable view of individual titles, filters for exploring catalog records, title details, and CSV export functionality for selected data.

## 📂 Dataset Information

**Dataset name:** Netflix Movies and TV Shows

**Dataset source:** [Netflix Movies and TV Shows — Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)

**Original dataset size:** 8,807 records and 12 columns.

The dataset includes the following fields:

- `show_id` — Unique identifier for a title
- `type` — Movie or TV Show
- `title` — Title name
- `director` — Director information
- `cast` — Cast information
- `country` — Country associated with the title
- `date_added` — Date the title was added to Netflix
- `release_year` — Original release year
- `rating` — Content maturity rating
- `duration` — Movie runtime or number of TV show seasons
- `listed_in` — Genres or categories
- `description` — Title description

**Dataset note:** This dataset contains catalog metadata. It does not provide actual viewing hours, revenue, subscription numbers, or individual viewer engagement.

## 🧹 Data Cleaning and Preparation

The project involves preparing the dataset for analysis and visualization. Depending on the processing implemented in the application, this includes:

- Inspecting columns, data types, and missing values.
- Handling missing or inconsistent information.
- Processing date and duration fields.
- Preparing genre and country information for analysis.
- Creating derived fields for additional analytical comparisons.
- Organizing data for interactive charts and filtering.

Missing values and derived metrics should be interpreted according to the cleaning rules used in the application.

## 🚀 Installation and Execution

### Prerequisites

- Python 3.10 or a compatible Python version.
- pip package manager.
- The project files and Netflix dataset.

### Step 1: Open the Project Folder

Place the project files in one folder. Ensure the dataset `netflix_titles.csv` is available at the path expected by the Python application.

### Step 2: Install Dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

The main Python file is:

`TusheetKaurBhatia_NetflixContentAnalytics.py`

Start the dashboard using:

```bash
streamlit run TusheetKaurBhatia_NetflixContentAnalytics.py
```

### Step 4: Open the Dashboard

After the application starts, open the local URL displayed in the terminal. The default Streamlit address is:

**http://localhost:8501**

You can now interact with the dashboard, explore visualizations, apply filters, and search for titles.

## 📈 Analytical Outcomes

The dashboard supports exploration of:

- The balance between movies and TV shows.
- Changes in catalog additions over time.
- Genre distribution and content categories.
- Country-wise catalog representation.
- Maturity rating and duration patterns.
- Individual title information through interactive search and filtering.

All conclusions should be based on the results displayed by the application and the underlying dataset. Catalog counts alone do not establish a title's popularity or commercial success.

## ⚠️ Limitations

- The dataset represents catalog information and may not reflect Netflix's current library.
- Viewing hours, revenue, subscriptions, and audience engagement are not available.
- Some records contain missing information.
- Titles associated with multiple countries or genres may contribute to multiple category counts.
- Derived metrics depend on the definitions and assumptions used during data preparation.
- Historical patterns should not be interpreted as predictions of future performance.

## 🔮 Future Enhancements

- Integrate regularly updated catalog data.
- Add advanced time-series analysis.
- Apply natural language processing to title descriptions.
- Introduce additional filtering and reporting options.
- Integrate external datasets for further analysis where appropriate.
- Extend the dashboard with additional analytical metrics.

## 👩‍💻 Author

**Tusheet Kaur Bhatia**

**Project Title:** Netflix Content Analytics Dashboard

**Project Type:** Data Analytics

## 📄 Data Attribution

The project uses the Netflix Movies and TV Shows dataset available on Kaggle. Dataset attribution and applicable usage terms should be respected when sharing or redistributing the data.

This project is intended for educational and analytical purposes.

---

*Developed using Python, Pandas, Streamlit, and Plotly.*