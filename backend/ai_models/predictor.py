# predictor.py

import pandas as pd
from prophet import Prophet

def predict_traffic():
    df = pd.read_csv('../data_collection/traffic_data.csv')
    df = df.rename(columns={'travel_time_mins': 'y'})
    df['ds'] = pd.date_range(start='2025-05-08', periods=len(df), freq='15min')
    df = df[['ds', 'y']]

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=12, freq='15min')  # Predict next 3 hours
    forecast = model.predict(future)

    forecast[['ds', 'yhat']].to_csv('traffic_prediction.csv', index=False)
    print("✅ Traffic prediction saved to traffic_prediction.csv")

def predict_aqi():
    df = pd.read_csv('../data_collection/aqi_data_combined.csv')
    df = df.rename(columns={'value': 'y'})
    df['ds'] = pd.date_range(start='2025-05-08', periods=len(df), freq='15min')
    df = df[['ds', 'y']]

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=12, freq='15min')  # Predict next 3 hours
    forecast = model.predict(future)

    forecast[['ds', 'yhat']].to_csv('aqi_prediction.csv', index=False)
    print("✅ AQI prediction saved to aqi_prediction.csv")

if __name__ == "__main__":
    predict_traffic()
    predict_aqi()
