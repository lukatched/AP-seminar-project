import requests
import json

# Load config from JSON file
with open('src/data/raw/micronutrient.json') as f:
    config = json.load(f)

# Prepare the request headers
headers = {
    'Content-Type': 'application/json',
    'x-app-id': config['appId'],  # Assuming appId is stored in the JSON
    'x-app-key': config['api_key']
}

# Prepare the request body
body = {
    "query": config['search_term']  # Using the search term from the JSON
}

# Make the API request
try:
    response = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', headers=headers, json=body)
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

