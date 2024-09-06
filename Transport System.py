import pandas as pd
from sklearn.cluster import KMeans

## Analyzing Ticketing Data to Understand Passenger Flows

# Load ticketing data into a pandas DataFrame
df =pd.read_csv(r"C:\Users\mitta\OneDrive\Desktop\Hackathon\ticketing_data.csv")


# Extract origin and destination stops from the data
origins = df['origin_stop']
destinations = df['destination_stop'] 

# Perform clustering analysis to identify common passenger flows
kmeans = KMeans(n_clusters=5).fit(df[['origin_lat', 'origin_lon', 'dest_lat', 'dest_lon']])
df['passenger_flow'] = kmeans.labels_

# Analyze results to understand major passenger flows
passenger_flows = df.groupby(['passenger_flow', 'origin_stop', 'destination_stop']).size().reset_index(name='count')
print(passenger_flows.sort_values('count', ascending=False).head(10))

# Make service adjustments based on the identified flows
# e.g. increase frequency on high demand routes

## Enabling Demand-Responsive Transport

import requests
import time

# Function to get current passenger demand from ticketing system
def get_current_demand():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        response.raise_for_status()  # Raise exception for 4xx or 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current demand: {e}")
        return None

# Function to get current vehicle locations from GPS
def get_vehicle_locations():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching vehicle locations: {e}")
        return None

# Function to optimize routes based on demand and vehicle locations  
def optimize_routes(demand, locations):
    # Implement route optimization logic here
    # This is a placeholder for demonstration purposes
    optimized_routes = {'routes': [
        {'vehicle_id': 'Vehicle_1', 'route': ['Stop A', 'Stop B', 'Stop C']},
        {'vehicle_id': 'Vehicle_2', 'route': ['Stop D', 'Stop E', 'Stop F']}
    ]}
    return optimized_routes

# Function to dispatch route assignments to vehicles
def dispatch_routes(routes):
    try:
        response = requests.post('https://jsonplaceholder.typicode.com/users', json=routes)
        response.raise_for_status()
        print("Route assignments dispatched successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error dispatching route assignments: {e}")

# Continuously monitor passenger demand and vehicle locations
while True:
    current_demand = get_current_demand()
    vehicle_locations = get_vehicle_locations()
    
    if current_demand and vehicle_locations:
        optimized_routes = optimize_routes(current_demand, vehicle_locations)
        dispatch_routes(optimized_routes)
    
    time.sleep(300)  # Wait for 5 minutes before repeating optimization