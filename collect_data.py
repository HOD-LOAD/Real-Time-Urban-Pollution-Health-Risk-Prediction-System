import requests
import pandas as pd
import time

API_KEY = "9e94b6dbe3aabf3887d8583ee4c862a5"   
LAT, LON = 28.7041, 77.1025  # Delhi (change if needed)

def fetch_data():
    # Pollution API
    pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
    pollution_res = requests.get(pollution_url).json()

    # Weather API
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    weather_res = requests.get(weather_url).json()

    if "list" in pollution_res and "main" in weather_res:
        return {
            # Timestamp
            "timestamp": pd.to_datetime(pollution_res["list"][0]["dt"], unit="s"),

            # Pollution
            "aqi": pollution_res["list"][0]["main"]["aqi"],
            "co": pollution_res["list"][0]["components"]["co"],
            "no": pollution_res["list"][0]["components"]["no"],
            "no2": pollution_res["list"][0]["components"]["no2"],
            "o3": pollution_res["list"][0]["components"]["o3"],
            "so2": pollution_res["list"][0]["components"]["so2"],
            "pm2_5": pollution_res["list"][0]["components"]["pm2_5"],
            "pm10": pollution_res["list"][0]["components"]["pm10"],
            "nh3": pollution_res["list"][0]["components"]["nh3"],

            # Weather
            "temperature": weather_res["main"]["temp"],
            "humidity": weather_res["main"]["humidity"],
            "pressure": weather_res["main"]["pressure"],
            "wind_speed": weather_res["wind"]["speed"],
            "weather": weather_res["weather"][0]["description"]
        }
    else:
        print(" API Error:", pollution_res, weather_res)
        return None

#  Collect data (every 1 min for demo)
for i in range(1000):  # collect samples then stop
    record = fetch_data()
    if record:
        df = pd.DataFrame([record])
        try:
            old_df = pd.read_csv("pollution_data.csv")
            df = pd.concat([old_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_csv("pollution_data.csv", index=False)
        print(f" Logged {i+1}:", record)

    time.sleep(3600)  # wait 1 hrs
