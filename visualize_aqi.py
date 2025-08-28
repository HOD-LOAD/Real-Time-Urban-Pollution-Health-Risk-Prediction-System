# visualize_all_cities.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load predicted AQI results
df = pd.read_csv("predicted_aqi_results.csv")

# Convert Datetime to datetime type
df['Datetime'] = pd.to_datetime(df['Datetime'])

# -------------------------
# 1. Plot AQI trends for all cities
# -------------------------
plt.figure(figsize=(14,7))
cities = df['City'].unique()

for city in cities:
    city_data = df[df['City'] == city]
    sns.lineplot(x='Datetime', y='Predicted_AQI', data=city_data, label=city)

plt.title("Predicted AQI Trends Over Time - All Cities")
plt.xlabel("Date")
plt.ylabel("Predicted AQI")
plt.xticks(rotation=45)
plt.legend(title="City")
plt.tight_layout()
plt.show()

# -------------------------
# 2. Highlight top 10 most polluted days across all cities
# -------------------------
top_polluted = df.sort_values(by='Predicted_AQI', ascending=False).head(10)
plt.figure(figsize=(10,6))
sns.barplot(x='Datetime', y='Predicted_AQI', hue='City', data=top_polluted, dodge=False, palette="Reds_r")
plt.title("Top 10 Most Polluted Days Across All Cities")
plt.ylabel("Predicted AQI")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------
# 3. Heatmap of monthly average AQI per city
# -------------------------
df['Month'] = df['Datetime'].dt.to_period('M')
monthly_avg = df.groupby(['Month', 'City'])['Predicted_AQI'].mean().unstack()
plt.figure(figsize=(12,6))
sns.heatmap(monthly_avg.T, cmap='Reds', cbar_kws={'label': 'Average AQI'})
plt.title("Monthly Average AQI Heatmap by City")
plt.xlabel("Month")
plt.ylabel("City")
plt.tight_layout()
plt.show()

