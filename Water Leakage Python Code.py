import pandas as pd
import numpy as np
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt



# Load data
data = pd.read_csv(r"C:\Users\mitta\OneDrive\Desktop\Hackathon\water_meter_data - Copy.csv")

# Check the first few rows to confirm the structure and presence of the location column
print(data.head())

# Preprocess data
data['timestamp'] = pd.to_datetime(data['timestamp'])
data['water_meter_reading'] = pd.to_numeric(data['water_meter_reading'], errors='coerce')
data = data.dropna()

# Ensure 'location' column exists and has valid values
if 'location' not in data.columns:
    raise ValueError("The 'location' column is missing from the data.")
    
# Feature engineering
data['delta_water'] = data['water_meter_reading'].diff()
data['avg_water_consumption_rate'] = data['delta_water'] / data['timestamp'].diff().dt.total_seconds()
data['std_dev_water_consumption_rate'] = data['avg_water_consumption_rate'].rolling(window=10).std()

# Filling NaN values created due to diff() and rolling() operations
data[['avg_water_consumption_rate', 'std_dev_water_consumption_rate']] = data[['avg_water_consumption_rate', 'std_dev_water_consumption_rate']].fillna(0)

# Anomaly detection
scaler = StandardScaler()
data[['avg_water_consumption_rate', 'std_dev_water_consumption_rate']] = scaler.fit_transform(data[['avg_water_consumption_rate', 'std_dev_water_consumption_rate']])

ocsvm = OneClassSVM(kernel='rbf', gamma=0.1, nu=0.1)
ocsvm.fit(data[['avg_water_consumption_rate', 'std_dev_water_consumption_rate']])

# Predict anomalies
anomaly_scores = ocsvm.decision_function(data[['avg_water_consumption_rate', 'std_dev_water_consumption_rate']])
anomaly_labels = ocsvm.predict(data[['avg_water_consumption_rate', 'std_dev_water_consumption_rate']])

# Leakage detection with location
leakage_alerts = []
for i in range(len(anomaly_labels)):
    if anomaly_labels[i] == -1:
        if data['avg_water_consumption_rate'].iloc[i] > data['avg_water_consumption_rate'].mean() + 2 * data['std_dev_water_consumption_rate'].mean():
            leakage_alerts.append((data['timestamp'].iloc[i], data['water_meter_reading'].iloc[i], data['location'].iloc[i]))

# Print leakage alerts with location
for alert in leakage_alerts:
    print(f"Potential water leakage detected at {alert[0]} in {alert[2]} with water meter reading {alert[1]}")

# Optional: Visualize the results
plt.figure(figsize=(12, 6))
plt.scatter(data['timestamp'], data['avg_water_consumption_rate'], c=anomaly_labels, cmap='coolwarm', label='Anomaly Detection')
plt.xlabel('Timestamp')
plt.ylabel('Average Water Consumption Rate')
plt.title('Water Consumption Anomaly Detection')
plt.legend()
plt.show()