

import streamlit as st
import pandas as pd
import plotly.express as px
import folium

from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Business Recommendation System",
    page_icon="📍",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Business Selection")

business_type = st.sidebar.selectbox(
    "Choose Business Type",
    ["Cafe", "Xerox Shop"]
)

# =====================================================
# LOAD DATA
# =====================================================

if business_type == "Cafe":
    df = pd.read_csv("cafe_features_dataset.csv")
else:
    df = pd.read_csv("xeroxfeaturesdataset.csv")

# =====================================================
# MACHINE LEARNING
# =====================================================

if "Cluster" not in df.columns:

    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    if business_type == "Cafe":

        features = df[
            [
                "Cafes",
                "Colleges",
                "Schools",
                "Offices"
            ]
        ]

    else:

        features = df[
            [
                "Schools",
                "Colleges",
                "Offices",
                "BusStops",
                "XeroxShops"
            ]
        ]

    scaler = StandardScaler()

    X = scaler.fit_transform(features)

    kmeans = KMeans(
        n_clusters=4,
        random_state=42
    )

    df["Cluster"] = kmeans.fit_predict(X)

# =====================================================
# OPPORTUNITY SCORE
# =====================================================

if "Opportunity_Score" not in df.columns:

    if business_type == "Cafe":

        df["Opportunity_Score"] = (
            4 * df["Colleges"]
            + 3 * df["Offices"]
            + 1 * df["Schools"]
            - 2 * df["Cafes"]
        )

    else:

        df["Opportunity_Score"] = (
            5 * df["Colleges"]
            + 4 * df["Schools"]
            + 3 * df["Offices"]
            + 1 * df["BusStops"]
            - 4 * df["XeroxShops"]
        )

# =====================================================
# SORT DATA
# =====================================================

df = df.sort_values(
    by="Opportunity_Score",
    ascending=False
)

# =====================================================
# REVERSE GEOCODING
# =====================================================

geolocator = Nominatim(
    user_agent="business_recommendation"
)

@st.cache_data
def get_area(lat, lon):

    try:

        location = geolocator.reverse(
            (lat, lon),
            exactly_one=True,
            timeout=10
        )

        if location:
            return location.address.split(",")[0]

        return "Unknown"

    except:
        return "Unknown"

if "Area" not in df.columns:

    top_rows = min(20, len(df))

    areas = []

    for i in range(top_rows):

        areas.append(
            get_area(
                df.iloc[i]["Latitude"],
                df.iloc[i]["Longitude"]
            )
        )

    remaining = ["Unknown"] * (len(df) - top_rows)

    df["Area"] = areas + remaining


# Remove duplicate area names
df = df.drop_duplicates(
    subset=["Area"],
    keep="first"
).reset_index(drop=True)
# =====================================================
# TITLE
# =====================================================

if business_type == "Cafe":

    st.title("☕ Cafe Business Recommendation System")

    st.markdown(
        "AI-powered system to identify the best locations for opening a cafe."
    )

else:

    st.title("📄 Xerox Shop Recommendation System")

    st.markdown(
        "AI-powered system to identify the best locations for opening a Xerox shop."
    )

# =====================================================
# FILTERS
# =====================================================

top_n = st.sidebar.slider(
    "Top Locations",
    1,
    min(20, len(df)),
    10
)




# =====================================================
# BEST LOCATION
# =====================================================

best = df.iloc[0]

st.subheader("🏆 Best Recommended Area")

st.info(f"{best['Area']}")

# =====================================================
# TABLE
# =====================================================

# =====================================================
# TOP RECOMMENDED AREAS
# =====================================================

st.subheader("📍 Top Recommended Areas")

top_locations = df.head(top_n)

for i, (_, row) in enumerate(top_locations.iterrows(), start=1):

    with st.expander(f"{i}. {row['Area']}"):

        st.write(
            f"📈 Opportunity Score: {row['Opportunity_Score']}"
        )

        if business_type == "Cafe":

            st.write(
                f"☕ Cafes Nearby: {row['Cafes']}"
            )

            st.write(
                f"🎓 Colleges Nearby: {row['Colleges']}"
            )

            st.write(
                f"🏫 Schools Nearby: {row['Schools']}"
            )

            st.write(
                f"🏢 Offices Nearby: {row['Offices']}"
            )

        else:

            st.write(
                f"🎓 Colleges Nearby: {row['Colleges']}"
            )

            st.write(
                f"🏫 Schools Nearby: {row['Schools']}"
            )

            st.write(
                f"🏢 Offices Nearby: {row['Offices']}"
            )

            st.write(
                f"🚌 Bus Stops Nearby: {row['BusStops']}"
            )

            st.write(
                f"📄 Existing Xerox Shops Nearby: {row['XeroxShops']}"
            )
# =====================================================
# MAP
# =====================================================

st.subheader("🗺 Recommended Locations Map")

m = folium.Map(
    location=[
        best["Latitude"],
        best["Longitude"]
    ],
    zoom_start=12
)

for _, row in df.head(top_n).iterrows():

    popup_text = f"""
    Area: {row['Area']}<br>
    Score: {row['Opportunity_Score']}
    """

    folium.Marker(
        [
            row["Latitude"],
            row["Longitude"]
        ],
        popup=popup_text
    ).add_to(m)

st_folium(
    m,
    width=1200,
    height=500
)

# =====================================================
# CLUSTER VISUALIZATION
# =====================================================

st.subheader("📊 AI Cluster Analysis")

fig = px.scatter(
    df,
    x="Longitude",
    y="Latitude",
    color=df["Cluster"].astype(str),
    size="Opportunity_Score",
    hover_name="Area",
    title="Business Location Clusters"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.subheader("📈 Business Insights")

if business_type == "Cafe":

    st.info(
        """
Recommendation Factors:

• Colleges Nearby

• Offices Nearby

• Schools Nearby

• Existing Cafe Competition

Higher demand and lower competition produce better scores.
"""
    )

else:

    st.info(
        """
Recommendation Factors:

• Colleges Nearby

• Schools Nearby

• Offices Nearby

• Bus Stops Nearby

• Existing Xerox Shop Competition

Higher student and office demand with lower competition produces better scores.
"""
    )


# =====================================================
# DETAILED ANALYSIS
# =====================================================

show_details = st.checkbox(
    "Show Detailed Analysis"
)

if show_details:

    st.subheader("Detailed Recommendation Data")

    if business_type == "Cafe":

        detailed_df = df.head(top_n)[
            [
                "Area",
                "Latitude",
                "Longitude",
                "Cafes",
                "Colleges",
                "Schools",
                "Offices",
                "Cluster",
                "Opportunity_Score"
            ]
        ]

    else:

        detailed_df = df.head(top_n)[
            [
                "Area",
                "Latitude",
                "Longitude",
                "Schools",
                "Colleges",
                "Offices",
                "BusStops",
                "XeroxShops",
                "Cluster",
                "Opportunity_Score"
            ]
        ]

    st.dataframe(
        detailed_df,
        use_container_width=True
    )


show_metrics = st.checkbox(
    "Show Technical Details"
)

if show_metrics:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Locations Analyzed",
        len(df)
    )

    col2.metric(
        "Best Score",
        int(df["Opportunity_Score"].max())
    )

    col3.metric(
        "Clusters Found",
        df["Cluster"].nunique()
    )

# =====================================================
# DOWNLOAD
# =====================================================

st.download_button(
    label="⬇ Download Recommendations",
    data=df.to_csv(index=False),
    file_name=f"{business_type.lower().replace(' ','_')}_recommendations.csv",
    mime="text/csv"
)



