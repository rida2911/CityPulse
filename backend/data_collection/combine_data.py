import pandas as pd

# Load both CSV files
traffic_df = pd.read_csv("traffic_data.csv")
aqi_df = pd.read_csv("pollution_data.csv")

# Extract city name from traffic route (e.g., "Bhopal → Indore" → "Bhopal")
traffic_df["city"] = traffic_df["route"].apply(lambda x: x.split("→")[0].strip())

# Convert timestamp to datetime
traffic_df["timestamp"] = pd.to_datetime(traffic_df["timestamp"])
aqi_df["timestamp"] = pd.to_datetime(aqi_df["timestamp"])

# Round timestamp to nearest hour for easier merging
traffic_df["rounded_time"] = traffic_df["timestamp"].dt.round("H")
aqi_df["rounded_time"] = aqi_df["timestamp"].dt.round("H")

# Merge on city + time
merged_df = pd.merge(
    traffic_df,
    aqi_df,
    left_on=["city", "rounded_time"],
    right_on=["city", "rounded_time"],
    how="inner"
)

# Drop extra columns if needed
merged_df = merged_df[[
    "route", "distance_km", "travel_time_mins", "traffic_delay_mins",
    "city", "aqi", "pm2_5", "pm10", "timestamp_x"
]]
merged_df.rename(columns={"timestamp_x": "timestamp"}, inplace=True)

# Save final dataset
merged_df.to_csv("combined_city_data.csv", index=False)
print("✅ Combined data saved as combined_city_data.csv")
