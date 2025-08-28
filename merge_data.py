import pandas as pd

# Load both datasets
live = pd.read_csv("pollution_data.csv")
kaggle = pd.read_csv("Air_quality_data.csv")

# Standardize column names
kaggle.rename(columns={
    "pm2.5": "pm2_5",
    "pm10": "pm10",
    "no2": "no2",
    "so2": "so2",
    "co": "co",
    "o3": "o3",
    "date": "timestamp"
}, inplace=True)

# Combine
combined = pd.concat([kaggle, live], ignore_index=True)

# Save
combined.to_csv("combined_data.csv", index=False)

print("✅ Merged dataset saved as combined_data.csv")
