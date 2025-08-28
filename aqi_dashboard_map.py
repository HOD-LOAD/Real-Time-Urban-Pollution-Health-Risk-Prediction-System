# aqi_dashboard_map.py

import pandas as pd
import streamlit as st
import plotly.express as px

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("predicted_aqi_results.csv")
df['Datetime'] = pd.to_datetime(df['Datetime'])

st.title("🌆 Urban Air Quality Dashboard with Map")
st.write("Explore predicted AQI trends, categories, and city-wise pollution map.")

# -------------------------
# Sidebar filters
# -------------------------
cities = df['City'].unique()
selected_cities = st.sidebar.multiselect("Select Cities", cities, default=cities)

start_date = st.sidebar.date_input("Start Date", df['Datetime'].min())
end_date = st.sidebar.date_input("End Date", df['Datetime'].max())

# Filter data based on selections
filtered_df = df[
    (df['City'].isin(selected_cities)) &
    (df['Datetime'] >= pd.to_datetime(start_date)) &
    (df['Datetime'] <= pd.to_datetime(end_date))
]

# -------------------------
# AQI Trends Line Chart
# -------------------------
st.subheader("AQI Trends Over Time")
fig_line = px.line(
    filtered_df, x='Datetime', y='Predicted_AQI', color='City',
    labels={'Predicted_AQI': 'Predicted AQI'}, title="AQI Trends"
)
st.plotly_chart(fig_line, use_container_width=True)

# -------------------------
# AQI Category Distribution
# -------------------------
st.subheader("AQI Category Distribution")
fig_bar = px.histogram(
    filtered_df, x='AQI_Category', color='City', barmode='group',
    category_orders={"AQI_Category": ["Good","Satisfactory","Moderate","Poor","Very Poor","Severe"]},
    title="AQI Category Counts"
)
st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------
# Top N Most Polluted Days
# -------------------------
st.subheader("Top Polluted Days")
top_n = st.slider("Select Top N Days", 5, 20, 10)
top_polluted = filtered_df.sort_values(by='Predicted_AQI', ascending=False).head(top_n)
fig_top = px.bar(
    top_polluted, x='Datetime', y='Predicted_AQI', color='City',
    title=f"Top {top_n} Most Polluted Days"
)
st.plotly_chart(fig_top, use_container_width=True)

# -------------------------
# City coordinates
# -------------------------
city_coords = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Bangalore": (12.9716, 77.5946)
}

# -------------------------
# Static City-wise AQI Map
# -------------------------
st.subheader("City-wise AQI Map (Latest Date)")
latest_aqi = filtered_df.groupby('City').last().reset_index()
latest_aqi['lat'] = latest_aqi['City'].map(lambda x: city_coords.get(x, (0,0))[0])
latest_aqi['lon'] = latest_aqi['City'].map(lambda x: city_coords.get(x, (0,0))[1])

fig_map = px.scatter_geo(
    latest_aqi,
    lat='lat',
    lon='lon',
    color='Predicted_AQI',
    size='Predicted_AQI',
    hover_name='City',
    color_continuous_scale='Reds',
    range_color=[0, 500],
    size_max=40,
    title="City-wise Predicted AQI (Latest Date)"
)
fig_map.update_geos(
    visible=True,
    resolution=50,
    showcountries=True,
    countrycolor="Black",
    showland=True,
    landcolor="LightGreen",
    showocean=True,
    oceancolor="LightBlue",
    scope='asia'
)
st.plotly_chart(fig_map, use_container_width=True)

# -------------------------
# Animated City-wise AQI Map
# -------------------------
st.subheader("Animated City-wise AQI Map Over Time")
filtered_df['lat'] = filtered_df['City'].map(lambda x: city_coords.get(x, (0,0))[0])
filtered_df['lon'] = filtered_df['City'].map(lambda x: city_coords.get(x, (0,0))[1])

fig_anim = px.scatter_geo(
    filtered_df,
    lat='lat',
    lon='lon',
    color='Predicted_AQI',
    size='Predicted_AQI',
    hover_name='City',
    animation_frame=filtered_df['Datetime'].dt.strftime('%Y-%m-%d'),
    color_continuous_scale='Reds',
    range_color=[0, 500],
    size_max=40,
    title="Animated City-wise Predicted AQI Over Time",
    scope='asia'
)
fig_anim.update_geos(
    visible=True,
    resolution=50,
    showcountries=True,
    countrycolor="Black",
    showland=True,
    landcolor="LightGreen",
    showocean=True,
    oceancolor="LightBlue"
)
st.plotly_chart(fig_anim, use_container_width=True)

# -------------------------
# Optional: Show raw data
# -------------------------
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
