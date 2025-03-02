import os
import pandas as pd
from difflib import get_close_matches

# Define file paths
food_csv_path = 'data/raw/FlavorDB/Food.csv'
common_foods_csv_path = 'data/raw/FlavorDB/common_foods.csv'

# Check if the common foods file exists
if not os.path.exists(common_foods_csv_path):
    print(f"Error: {common_foods_csv_path} not found.")
    exit(1)

# Load the datasets
food_df = pd.read_csv(food_csv_path)
common_foods_df = pd.read_csv(common_foods_csv_path)

# Normalize the food names to lowercase
food_df['name'] = food_df['name'].str.lower()
common_foods_df['name'] = common_foods_df['name'].str.lower()

# Create a set of common food names for quick lookup
common_foods_set = set(common_foods_df['name'])

# Function to find the closest match for a food name
def find_closest_match(food_name, common_foods_set):
    matches = get_close_matches(food_name, common_foods_set, n=1, cutoff=0.8)
    return matches[0] if matches else None

# Filter and rename foods
filtered_foods = []
for index, row in food_df.iterrows():
    food_name = row['name']
    if food_name in common_foods_set:
        filtered_foods.append(row)
    else:
        closest_match = find_closest_match(food_name, common_foods_set)
        if closest_match:
            row['name'] = closest_match
            filtered_foods.append(row)

# Create a new DataFrame with the filtered and renamed foods
filtered_food_df = pd.DataFrame(filtered_foods)

# Save the filtered and updated Food.csv back to the file
filtered_food_df.to_csv(food_csv_path, index=False)

print("Filtered and updated Food.csv saved successfully.")
