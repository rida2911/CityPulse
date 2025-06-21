import pandas as pd

def suggest_best_route():
    traffic_df = pd.read_csv('C:/Users/hp/OneDrive/Desktop/CityPulse/backend/data_collection/traffic_data.csv')
    aqi_df = pd.read_csv('C:\Users\hp\OneDrive\Desktop\CityPulse\backend\data_collection\pollution_data.csv')

    # Simple average of both predictions (lower is better)
    combined_df = pd.DataFrame()
    combined_df['datetime'] = traffic_df['ds']
    combined_df['traffic_pred'] = traffic_df['yhat']
    combined_df['aqi_pred'] = aqi_df['yhat']

    # Normalized Score = traffic + aqi
    combined_df['score'] = combined_df['traffic_pred'] * 0.6 + combined_df['aqi_pred'] * 0.4

    # Best (lowest score) prediction row
    best = combined_df.loc[combined_df['score'].idxmin()]

    print(f"\n✅ Best Time to Travel: {best['datetime']}")
    print(f"Estimated Travel Time: {round(best['traffic_pred'],2)} mins")
    print(f"Estimated AQI Level: {round(best['aqi_pred'],2)}\n")

    combined_df.to_csv('route_suggestion.csv', index=False)
    print("✅ Route suggestion saved to route_suggestion.csv")

if __name__ == "__main__":
    suggest_best_route()

