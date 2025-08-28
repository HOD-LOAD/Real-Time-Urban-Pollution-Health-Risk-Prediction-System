# predict_aqi.py

import pandas as pd
import joblib

# Load saved model and preprocessor
model = joblib.load("aqi_model.pkl")
preprocessor = joblib.load("preprocessor.pkl")

# Load new data from CSV
# CSV should have columns: City, PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3
new_data = pd.read_csv("Air_quality_data.csv")

# Preprocess new data
X_new = preprocessor.transform(new_data)

# Predict AQI
predictions = model.predict(X_new)
new_data["Predicted_AQI"] = predictions

# Map predicted AQI to categories
def aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"

new_data["AQI_Category"] = new_data["Predicted_AQI"].apply(aqi_category)

# Save results to a new CSV
new_data.to_csv("predicted_aqi_results.csv", index=False)
print("✅ Predictions saved to predicted_aqi_results.csv")
print(new_data)
