# eda_visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ================================
# Load Kaggle dataset
# ================================
df = pd.read_csv("Air_quality_data.csv")

print("Dataset Shape:", df.shape)
print("\nDataset Preview (first 10 rows):")
print(df.head(10))

# ================================
# Clean Data
# ================================
# Convert Datetime column to proper datetime format
df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")

# Drop rows with missing datetime
df = df.dropna(subset=["Datetime"])

# Drop duplicates
df = df.drop_duplicates()

# Fill numeric missing values with median
df = df.fillna(df.median(numeric_only=True))

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# ================================
# Visualization 1: PM2.5 Trend
# ================================
plt.figure(figsize=(12,6))
for city in df["City"].unique()[:5]:  # Show only first 5 cities for clarity
    subset = df[df["City"] == city]
    plt.plot(subset["Datetime"], subset["PM2.5"], label=city)

plt.title("PM2.5 Trend Over Time (Sample Cities)")
plt.xlabel("Date")
plt.ylabel("PM2.5")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ================================
# Visualization 2: Distribution of AQI
# ================================
plt.figure(figsize=(8,5))
sns.histplot(df["AQI"], bins=30, kde=True)
plt.title("Distribution of AQI")
plt.xlabel("AQI")
plt.ylabel("Frequency")
plt.show()

# ================================
# Visualization 3: AQI Buckets Count
# ================================
plt.figure(figsize=(8,5))
sns.countplot(data=df, x="AQI_Bucket", order=df["AQI_Bucket"].value_counts().index)
plt.title("Count of AQI Buckets")
plt.xlabel("AQI Category")
plt.ylabel("Count")
plt.xticks(rotation=30)
plt.show()

# ================================
# Visualization 4: Correlation Heatmap
# ================================
plt.figure(figsize=(10,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap of Pollutants")
plt.show()

# ================================
# Visualization 5: Boxplot for PM2.5 by City
# ================================
plt.figure(figsize=(12,6))
sns.boxplot(data=df, x="City", y="PM2.5")
plt.title("PM2.5 Distribution Across Cities")
plt.xticks(rotation=45)
plt.show()
