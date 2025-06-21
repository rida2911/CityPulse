import requests
import pandas as pd
from datetime import datetime
import os

# 🔐 Your OpenWeatherMap API Key
API_KEY = '9d0486b29461947e3a5fdd4989c496d2'

# 📍 All City Coordinates (including MP)
city_coords = {
    # Metro Cities
    'Delhi': (28.6139, 77.2090),
    'Mumbai': (19.0760, 72.8777),
    'Bengaluru': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867),
    'Kolkata': (22.5726, 88.3639),
    'Chennai': (13.0827, 80.2707),
    'Ahmedabad': (23.0225, 72.5714),
    'Pune': (18.5204, 73.8567),
    'Jaipur': (26.9124, 75.7873),

    # MP Cities
    'Bhopal': (23.2599, 77.4126),
    'Indore': (22.7196, 75.8577),
    'Jabalpur': (23.1815, 79.9864),
    'Gwalior': (26.2183, 78.1828),
    'Ujjain': (23.1793, 75.7849)
}

def fetch_aqi_data():
    records = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for city, (lat, lon) in city_coords.items():
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        try:
            aqi = data['list'][0]['main']['aqi']  # AQI from 1 to 5
            components = data['list'][0]['components']
            records.append([
                city, lat, lon, aqi,
                components['pm2_5'], components['pm10'], components['no2'],
                components['so2'], components['o3'], components['co'],
                timestamp
            ])
        except:
            print(f"❌ Failed to fetch AQI for {city}")

    df = pd.DataFrame(records, columns=[
        'city', 'lat', 'lon', 'aqi',
        'pm2_5', 'pm10', 'no2', 'so2', 'o3', 'co', 'timestamp'
    ])

    file_exists = os.path.exists('pollution_data.csv')
    df.to_csv('pollution_data.csv', mode='a', index=False, header=not file_exists)
    print(f"✅ Fetched AQI for {len(records)} cities at {timestamp}")

if __name__ == "__main__":
    fetch_aqi_data()
