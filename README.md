# 📍 AI Business Recommendation System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![OpenStreetMap](https://img.shields.io/badge/Data-OpenStreetMap-7EAE53.svg)](https://www.openstreetmap.org/)

An end-to-end AI-powered geospatial analytics and decision-support system designed to determine optimal physical locations for launching new commercial businesses. By combining **OpenStreetMap (OSMnx)** spatial feature extraction, **Geodesic Distance Calculations**, **K-Means Clustering**, and custom **Opportunity Scoring Models**, this application converts raw geographic points of interest (POIs) into actionable business intelligence with an interactive **Streamlit** dashboard.

---

## 📋 Table of Contents

- [Overview & Problem Statement](#-overview--problem-statement)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Business Domains & Mathematical Scoring Models](#-business-domains--mathematical-scoring-models)
  - [1. Cafe Business Recommendation](#1-cafe-business-recommendation)
  - [2. Xerox / Printing Shop Recommendation](#2-xerox--printing-shop-recommendation)
- [Machine Learning & Data Pipeline](#-machine-learning--data-pipeline)
- [Repository Structure](#-repository-structure)
- [Prerequisites & Environment Setup](#-prerequisites--environment-setup)
- [Step-by-Step Installation & Quickstart](#-step-by-step-installation--quickstart)
- [Troubleshooting Common Issues](#-troubleshooting-common-issues)
- [Dashboard Walkthrough](#-dashboard-walkthrough)
- [Future Roadmap](#-future-roadmap)
- [License & Author](#-license--author)

---

## 🎯 Overview & Problem Statement

Selecting a physical location for a business significantly influences foot traffic, revenue, and long-term viability. Traditional location selection often relies on anecdotal evidence or expensive manual surveys. 

This project solves location selection by analyzing:
1. **Demand Drivers**: Nearby colleges, universities, schools, offices, and bus stops.
2. **Competitive Saturation**: Existing businesses of the same type within a 2 km radius.
3. **Geospatial Clustering**: Grouping candidate locations into clusters using unsupervised machine learning (`K-Means`).

---

## ✨ Key Features

- **🌐 Multi-Industry Support**: Dedicated models for both **Cafes** and **Xerox / Printing Shops**.
- **🗺️ Interactive Map Visualization**: Embedded **Folium** maps displaying optimal location pins, area names, and opportunity scores.
- **📊 AI Cluster Analytics**: Interactive **Plotly Express** scatter plots visualizing geospatial clusters sized by opportunity score.
- **🏷️ Automated Reverse Geocoding**: Real-time conversion of latitude/longitude coordinates into human-readable area names via **GeoPy / Nominatim**.
- **🎛️ Dynamic Filters**: Interactive sidebar sliders to filter top recommended zones (1 to 20 locations).
- **📥 CSV Data Export**: One-click download of generated location rankings with score breakdowns.
- **🛠️ Data Mining Notebook**: Included Jupyter Notebook (`recommend.ipynb`) demonstrating OSMnx POI extraction and grid location generator logic.

---

## 🏗️ System Architecture

```
                               ┌──────────────────────────────────┐
                               │     OpenStreetMap Data (OSM)     │
                               └────────────────┬─────────────────┘
                                                │
                                                ▼
                               ┌──────────────────────────────────┐
                               │  Geospatial Data Mining (OSMnx)  │
                               │  - Grid Generator (Lat/Lon)      │
                               │  - 2 km Geodesic Radius POI Count│
                               └────────────────┬─────────────────┘
                                                │
                                                ▼
                               ┌──────────────────────────────────┐
                               │      Feature Datasets (CSV)      │
                               │ - cafe_features_dataset.csv      │
                               │ - xeroxfeaturesdataset.csv       │
                               └────────────────┬─────────────────┘
                                                │
                                                ▼
                         ┌──────────────────────┴──────────────────────┐
                         │                                             │
                         ▼                                             ▼
       ┌──────────────────────────────────┐          ┌──────────────────────────────────┐
       │   K-Means Clustering Pipeline    │          │    Opportunity Scoring Engine    │
       │ - StandardScaler Features        │          │ - Demand (+) vs Competition (-)  │
       │ - 4-Cluster Partitioning         │          │ - Custom Weighted Formulations   │
       └────────────────┬─────────────────┘          └────────────────┬─────────────────┘
                        │                                             │
                        └──────────────────────┬──────────────────────┘
                                               │
                                               ▼
                               ┌──────────────────────────────────┐
                               │   Streamlit Web Application UI   │
                               │  - Reverse Geocoding (Nominatim) │
                               │  - Folium Interactive Maps       │
                               │  - Plotly Cluster Visualizations │
                               │  - CSV Export & Metrics Panel    │
                               └──────────────────────────────────┘
```

---

## 𝍠 Business Domains & Mathematical Scoring Models

### 1. Cafe Business Recommendation

For cafes, high foot traffic from students and office workers generates high revenue, while close proximity to competing cafes dampens potential market share.

* **Target Features**: `Colleges`, `Offices`, `Schools`, `Cafes`
* **Scoring Formula**:
  $$\text{Opportunity Score} = 4 \times \text{Colleges} + 3 \times \text{Offices} + 1 \times \text{Schools} - 2 \times \text{Cafes}$$

### 2. Xerox / Printing Shop Recommendation

Xerox and printing shops thrive near academic institutions (students printing assignments/notes), office spaces, and transit hubs (bus stops).

* **Target Features**: `Colleges`, `Schools`, `Offices`, `BusStops`, `XeroxShops`
* **Scoring Formula**:
  $$\text{Opportunity Score} = 5 \times \text{Colleges} + 4 \times \text{Schools} + 3 \times \text{Offices} + 1 \times \text{BusStops} - 4 \times \text{XeroxShops}$$

---

## 🤖 Machine Learning & Data Pipeline

1. **Feature Normalization**: Input features are scaled using `StandardScaler` from `scikit-learn` to ensure equal variance across all POI counts.
2. **Unsupervised Clustering**: `KMeans(n_clusters=4, random_state=42)` groups candidate spatial coordinates into distinct market archetypes (e.g., High-Density Academic, Corporate Hub, Residential, Low-Density Outer).
3. **Geodesic Distance Filtering**: Existing POIs are aggregated within a `RADIUS = 2000` meters (2 km) geodesic circle centered at each candidate coordinate.

---

## 📁 Repository Structure

```
Business-Recommendation/
├── app.py                      # Main Streamlit web application dashboard
├── recommend.ipynb             # Jupyter Notebook for dataset extraction & experimentation
├── cafe_features_dataset.csv   # Pre-computed feature dataset for Cafe locations
├── xeroxfeaturesdataset.csv    # Pre-computed feature dataset for Xerox shop locations
├── requirements.txt            # Python dependency requirements
├── LICENSE                     # MIT Open-Source License
└── README.md                   # Project Documentation
```

---

## ⚡ Prerequisites & Environment Setup

Before running the application, ensure you have the following installed on your system:

- **Python**: Version `3.8`, `3.9`, `3.10`, or `3.11` (Python 3.12+ users should ensure GIS C-libraries match dependency builds).
- **Git**: For cloning the repository.
- **Pip**: Latest version of `pip` (`python -m pip install --upgrade pip`).

---

## 🚀 Step-by-Step Installation & Quickstart

### Step 1: Clone the Repository
```bash
git clone https://github.com/dhanshreeg03/Business-Recommendation.git
cd Business-Recommendation
```

### Step 2: Create a Virtual Environment

**On Windows (PowerShell / Command Prompt):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
> 💡 **Note**: Make sure to include the `-r` flag when installing from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Step 4: Launch the Streamlit Web Dashboard

```bash
streamlit run app.py
```

Once launched, open your web browser and navigate to:
```
http://localhost:8501
```

---

## 🛠️ Troubleshooting Common Issues

### ❌ Error: `ERROR: Could not find a version that satisfies the requirement requirements.txt`
* **Cause**: Running `pip install requirements.txt` instead of using the `-r` flag.
* **Solution**: Use `pip install -r requirements.txt`.

### ❌ Error: `No module named venv1` or `conda is not recognized`
* **Cause**: Typo in the virtual environment module name (`venv1`) or Conda is not added to system PATH.
* **Solution**: Use standard Python venv: `python -m venv venv`.

### ❌ Error: Geocoding Timeout / Rate Limit (`Nominatim`)
* **Cause**: OpenStreetMap Nominatim API rate limits or network latency.
* **Solution**: The application uses `@st.cache_data` and caps initial area lookups to top rows. Ensure an active internet connection when running for the first time.

---

## 📊 Dashboard Walkthrough

1. **Sidebar Navigation**: Select between **Cafe** and **Xerox Shop** analysis options.
2. **Filter Controls**: Adjust the **Top Locations** slider (1 - 20 areas).
3. **Best Recommended Area**: Highlights the #1 ranked location banner.
4. **Top Recommended Areas**: Expandable list displaying exact opportunity scores and granular POI counts (Colleges, Offices, Schools, Bus Stops, Competitors).
5. **Interactive Map**: View pins on Folium map with area names and scores in popups.
6. **Cluster Scatter Plot**: Plotly visual showing spatial distribution colored by K-Means cluster and sized by opportunity score.
7. **CSV Download**: Click **Download Recommendations** to export results.

---

## 🔮 Future Roadmap

- [ ] Incorporate foot traffic demographic heatmaps.
- [ ] Add real estate rent & property price index variables into opportunity scoring.
- [ ] Support dynamic custom city selection via user text input in the Streamlit interface.
- [ ] Implement multi-criteria decision analysis (AHP / TOPSIS) algorithms.

---

## 📄 License & Author

* **Author**: Dhanshree Gedam ([@dhanshreeg03](https://github.com/dhanshreeg03))
* **License**: This project is licensed under the [MIT License](LICENSE).
