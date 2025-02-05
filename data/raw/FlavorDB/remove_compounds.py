import pandas as pd
import os

# filepath: /c:/Users/Luka Anthony/OneDrive/Documents/Food Project/data/raw/FlavorDB/remove_compounds.py

# Load the filtered food names from food.csv
food_df = pd.read_csv('data/raw/FlavorDB/Food.csv')
food_names = food_df['name'].str.lower().tolist()  # Assuming the column name is 'name'

# Inspect the columns in the Flavor.csv file
flavor_df = pd.read_csv('data/raw/FlavorDB/Flavor.csv')
print("Columns in Flavor.csv:", flavor_df.columns)

# Function to filter and rename flavors based on food names
def filter_and_rename_flavors(file_path, food_names, output_path, food_column):
    df = pd.read_csv(file_path)
    df[food_column] = df[food_column].str.lower()  # Normalize the food names in the flavor file
    filtered_df = df[df[food_column].isin(food_names)]
    
    # Rename the entries in Flavor.csv to match the names in food.csv
    food_name_mapping = {name.lower(): name for name in food_df['name']}
    filtered_df[food_column] = filtered_df[food_column].map(food_name_mapping)
    
    # Create the output directory if it does not exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    filtered_df.to_csv(output_path, index=False)
    print(f"Filtered and renamed data saved to {output_path}")

# Determine the correct column name for linking to food names
# Assuming the correct column name is 'name' based on the inspection
food_column = 'name'  # Update this based on the actual column name in Flavor.csv

# Filter and rename flavors in Flavor.csv
filter_and_rename_flavors(
    'data/raw/FlavorDB/Flavor.csv',
    food_names,
    'data/processed/Flavor_filtered.csv',
    food_column
)