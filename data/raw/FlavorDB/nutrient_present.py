import requests
import pandas as pd

# Define the API credentials
API_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
APP_ID = '81bcc29f'
APP_KEY = '64a2364aa967fdf9e38dec6d157cbbb4'

# Define the nutrients of interest
nutrient_ids = [324, 301, 303, 305, 309, 307, 430, 417, 404, 405]

# Load the CSV file into a DataFrame
food_df = pd.read_csv('data/raw/FlavorDB/Food.csv')

# Function to fetch nutrient data from Nutritionix
def fetch_nutrient_data(food_name):
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "query": food_name,
        "timezone": "US/Eastern"
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {food_name}: {response.status_code}")
        return None

# Function to check for specified nutrients and get their amounts
def check_nutrients(food_name, nutrient_data):
    nutrients = {nutrient_id: 0 for nutrient_id in nutrient_ids}
    if nutrient_data:
        for nutrient in nutrient_data['foods'][0]['full_nutrients']:
            if nutrient['attr_id'] in nutrient_ids:
                nutrients[nutrient['attr_id']] = nutrient['value']
    return nutrients

# Fetch nutrient data and check for specified nutrients for each food
nutrient_results = []
for food_name in food_df['name']:
    nutrient_data = fetch_nutrient_data(food_name)
    nutrients = check_nutrients(food_name, nutrient_data)
    nutrient_results.append({
        "food_name": food_name,
        **nutrients
    })



# Create a DataFrame from the results
nutrient_df = pd.DataFrame(nutrient_results)

# Save the results to a CSV file
output_csv_path = '/Users/lukaanthony/Documents/GitHub/AP-seminar-project/data/raw/FlavorDB/Food_Nutrients.csv'
nutrient_df.to_csv(output_csv_path, index=False)

print("Nutrient data saved successfully.")