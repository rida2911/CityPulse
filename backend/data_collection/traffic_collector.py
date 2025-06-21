import requests
import pandas as pd
import time
from datetime import datetime
import os

# === YOUR TOMTOM API KEY ===
API_KEY = 'vG8GAWnq0tsG2rYuSZZrUqWwo7rPpiao'

# === ROUTES: Already well defined ===
routes = {
    # Delhi NCR
    'India Gate → Connaught Place': [(28.6129, 77.2295), (28.6315, 77.2167)],
    'Noida Sec 18 → Gurgaon Cyber Hub': [(28.5700, 77.3210), (28.5046, 77.0967)],
    'IGI Airport → Rajiv Chowk': [(28.5562, 77.1000), (28.6328, 77.2197)],
    'Akshardham → Hauz Khas': [(28.6127, 77.2773), (28.5494, 77.2000)],
    'Ghaziabad → DLF Cyber City': [(28.6692, 77.4538), (28.4916, 77.0920)],

    # MP
    'Bhopal → Indore': [(23.2599, 77.4126), (22.7196, 75.8577)],
    'Jabalpur → Katni': [(23.1815, 79.9864), (23.8335, 80.4094)],
    'Gwalior → Jhansi': [(26.2183, 78.1828), (25.4484, 78.5696)],
    'Ujjain → Dewas': [(23.1793, 75.7849), (22.9623, 76.0508)],
    'Sagar → Bhopal': [(23.8388, 78.7378), (23.2599, 77.4126)],

    # Mumbai
    'Gateway of India → Bandra': [(18.9219, 72.8340), (19.0606, 72.8370)],
    'CST → Thane': [(18.9402, 72.8356), (19.2183, 72.9781)],
    'Navi Mumbai → Andheri': [(19.0330, 73.0297), (19.1197, 72.8465)],
    'Borivali → Colaba': [(19.2288, 72.8561), (18.9076, 72.8147)],
    'Juhu → Powai': [(19.1076, 72.8265), (19.1197, 72.9051)],

    # Bengaluru
    'Kempegowda Airport → MG Road': [(13.1986, 77.7066), (12.9756, 77.6050)],
    'Whitefield → Electronic City': [(12.9698, 77.7500), (12.8398, 77.6762)],
    'Yeshwantpur → Marathahalli': [(13.0295, 77.5510), (12.9557, 77.7005)],
    'KR Puram → Banashankari': [(13.0078, 77.6950), (12.9252, 77.5730)],
    'Indiranagar → Hebbal': [(12.9719, 77.6412), (13.0350, 77.5913)],

    # Hyderabad
    'Charminar → Hitech City': [(17.3616, 78.4747), (17.4505, 78.3817)],
    'Secunderabad → Gachibowli': [(17.4399, 78.4983), (17.4444, 78.3498)],
    'LB Nagar → Madhapur': [(17.3514, 78.5780), (17.4486, 78.3915)],
    'Banjara Hills → Koti': [(17.4196, 78.4485), (17.3845, 78.4867)],
    'Uppal → Jubilee Hills': [(17.4039, 78.5600), (17.4326, 78.4072)],


    # === Kolkata ===
    'Howrah → Park Street': [(22.5958, 88.2636), (22.5534, 88.3529)],
    'Airport → Esplanade': [(22.6545, 88.4467), (22.5678, 88.3497)],

    # === Chennai ===
    'Chennai Airport → Marina Beach': [(12.9900, 80.1693), (13.0500, 80.2824)],
    'T Nagar → Velachery': [(13.0424, 80.2338), (12.9780, 80.2214)],

    # === Jaipur ===
    'Jaipur Junction → Amer Fort': [(26.9196, 75.7878), (26.9931, 75.8514)],
    'JLN Marg → Malviya Nagar': [(26.8647, 75.8125), (26.8459, 75.8177)],

    # === Ahmedabad ===
    'SG Highway → Maninagar': [(23.0594, 72.5117), (22.9961, 72.6038)],
    'Sabarmati → Kalupur': [(23.0780, 72.5851), (23.0276, 72.6024)],

    # === Pune ===
    'Shivajinagar → Hinjewadi': [(18.5308, 73.8445), (18.5946, 73.7063)],
    'Hadapsar → Kothrud': [(18.4985, 73.9320), (18.5074, 73.8077)]
}

def collect_traffic_data():
    records = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for route, (origin, destination) in routes.items():
        url = f"https://api.tomtom.com/routing/1/calculateRoute/{origin[0]},{origin[1]}:{destination[0]},{destination[1]}/json?key={API_KEY}&traffic=true"
        response = requests.get(url)
        data = response.json()

        if 'routes' not in data:
            print(f"❌ API failed for {route}")
            continue

        summary = data['routes'][0]['summary']
        length = summary['lengthInMeters'] / 1000
        travel_time = summary['travelTimeInSeconds'] / 60
        traffic_delay = summary.get('trafficDelayInSeconds', 0) / 60

        records.append([
            route, round(length, 2), round(travel_time, 2),
            round(traffic_delay, 2), timestamp
        ])

    df = pd.DataFrame(records, columns=[
        'route', 'distance_km', 'travel_time_mins', 'traffic_delay_mins', 'timestamp'
    ])

    # Save or append to CSV
    file_exists = os.path.exists('traffic_data.csv')
    df.to_csv('traffic_data.csv', mode='a', index=False, header=not file_exists)
    print(f"✅ Collected {len(records)} routes at {timestamp}")

if __name__ == "__main__":
    while True:
        collect_traffic_data()
        print("⏰ Waiting 15 mins for next update...\n")
        time.sleep(900)  # wait 15 minutes
