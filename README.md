# Netflix Content Analytics Dashboard

An interactive data analytics project using Python, Pandas, Streamlit, and Plotly.

## 📌 About the Project

The **Netflix Content Analytics Dashboard** is an interactive data analytics project developed to explore and analyze Netflix movies and TV shows. It helps identify patterns and trends in content distribution, genres, ratings, release years, and country-wise availability.

The dashboard presents data through interactive charts and visualizations, making it easier to understand Netflix's content library.

## 🎯 Project Objectives

- Analyze the distribution of movies and TV shows.
- Explore content trends based on release years.
- Identify the distribution of different genres.
- Analyze content ratings and classifications.
- Explore country-wise content distribution.
- Present data through interactive visualizations.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming and data analysis |
| Pandas | Data cleaning and manipulation |
| Streamlit | Interactive dashboard development |
| Plotly | Interactive charts and visualizations |

## 📂 Dataset

This project uses the **Netflix Movies and TV Shows** dataset available on Kaggle.

**Dataset source:** [Netflix Movies and TV Shows – Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)

The dataset contains information such as:

- Show ID and title
- Director and cast
- Country
- Date added
- Release year
- Rating and duration
- Genre and description

**Note:** The CSV dataset is not included in this GitHub repository. Download it from Kaggle and place `netflix_titles.csv` in the location expected by the Python application.

## 📊 Dashboard Features

### 1. Content Distribution
Explore the distribution of movies and TV shows in the dataset.

### 2. Release Year Analysis
Understand how content is distributed across different release years.

### 3. Genre Analysis
Explore the variety and distribution of genres available in the dataset.

### 4. Rating Analysis
Analyze the ratings and classifications of Netflix titles.

### 5. Country-wise Analysis
Explore the country-wise distribution of content using the available dataset information.

### 6. Interactive Visualizations
Use interactive charts to explore the dataset and understand its patterns.

## 📁 Project Structure

```text
Netflix-Content-Analytics/
├── TusheetKaurBhatia_NetflixContentAnalytics.py
├── requirements.txt
├── README.md
└── TusheetKaurBhatia_ProjectReport.docx
```

**Note:** The dataset file `netflix_titles.csv` must be downloaded separately and placed in the location specified in the Python code.

## ⚙️ Installation and Setup

Follow these steps to run the dashboard on your computer.

### Step 1: Clone the Repository

```bash
git clone https://github.com/TusheetKaurBhatia/Netflix-Content-Analytics.git
```

### Step 2: Open the Project Folder

```bash
cd Netflix-Content-Analytics
```

### Step 3: Download the Dataset

1. Open the [Kaggle dataset page](https://www.kaggle.com/datasets/shivamb/netflix-shows).
2. Download the dataset and extract it if required.
3. Locate `netflix_titles.csv`.
4. Place it in the location expected by the Python application.

### Step 4: Install Dependencies

Make sure Python is installed, then run:

```bash
pip install -r requirements.txt
```

### Step 5: Run the Dashboard

```bash
streamlit run TusheetKaurBhatia_NetflixContentAnalytics.py
```

Once the application starts, Streamlit will display a local URL, usually `http://localhost:8501`.

Open this address in your browser to view the dashboard while it is running.

**Important:** The localhost URL works on your own computer while the application is running. It is not a public demo link. To allow your mentor and other users to access the dashboard online, the project must be deployed.

## 📈 Expected Outcomes

- Better understanding of Netflix's content library.
- Identification of content distribution and release-year patterns.
- Exploration of genre, rating, and country-wise trends.
- Presentation of data-driven observations through interactive visualizations.
- Practical experience with Python-based data analytics.

## ⚠️ Limitations

- The analysis depends on the quality and completeness of the dataset.
- Missing values may affect some visualizations.
- The dashboard does not automatically reflect live changes to Netflix's catalogue.
- The dataset must be downloaded separately.

## 🔮 Future Enhancements

- Deploy the dashboard online for public access.
- Add more interactive filters.
- Include additional visualizations and trend analysis.
- Update the dataset periodically.
- Improve the dashboard interface and user experience.

## 👩‍💻 Author

**Tusheet Kaur Bhatia**

## 🙌 Acknowledgement

The dataset used in this project is sourced from Kaggle. This project was developed for educational purposes to demonstrate skills in data analytics, Python programming, and interactive data visualization.

---

*Thank you for visiting this project!*
