# aqi_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# -------------------------
# 1. Load Data
# -------------------------
df = pd.read_csv("Air_quality_data.csv")
print("Dataset Loaded. Shape:", df.shape)
print(df.head())

# -------------------------
# 2. Preprocessing
# -------------------------

# Drop rows with missing AQI
df = df.dropna(subset=["AQI"])

# Drop columns we won't use directly
df = df.drop(columns=["AQI_Bucket", "Datetime"], errors="ignore")

# Separate features and target
X = df.drop(columns=["AQI"])
y = df["AQI"]

# Identify categorical and numerical columns
categorical_cols = ["City"]
numerical_cols = X.select_dtypes(include=np.number).columns.tolist()

# Apply OneHotEncoding to categorical columns and scale numerical columns
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_cols),
        ("cat", OneHotEncoder(sparse_output=False, drop='first'), categorical_cols)
    ]
)

X_processed = preprocessor.fit_transform(X)

# -------------------------
# 3. Train/Test Split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y, test_size=0.2, random_state=42
)

# -------------------------
# 4. Model Training
# -------------------------
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# -------------------------
# 5. Evaluation
# -------------------------
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Training Complete")
print("Mean Squared Error:", mse)
print("R² Score:", r2)

# -------------------------
# 6. Save Model + Preprocessor
# -------------------------
joblib.dump(model, "aqi_model.pkl")
joblib.dump(preprocessor, "preprocessor.pkl")

print("\nModel saved as aqi_model.pkl and preprocessor.pkl")
