import pandas as pd

# Load the CSV files into DataFrames
grouped_compounds_foods_df = pd.read_csv('data/processed/grouped.csv')
food_nutrients_df = pd.read_csv('data/raw/FlavorDB/Food_Nutrients.csv')

# Define the units for each column in Food_Nutrients.csv
units = {
    '324': 'mg',  # Calcium
    '301': 'mg',  # Iron
    '303': 'mg',  # Magnesium
    '305': 'mg',  # Phosphorus
    '309': 'mg',  # Potassium
    '307': 'mg',  # Sodium
    '430': 'µg',  # Vitamin A
    '417': 'µg',  # Folate
    '404': 'mg',  # Vitamin B1
    '405': 'mg'   # Vitamin B2
}

# Function to append units to each value
def append_units(value, unit):
    if pd.isna(value):
        return value
    return f"{value}{unit}"

# Apply the units to each column in Food_Nutrients.csv
for column, unit in units.items():
    if column in food_nutrients_df.columns:
        food_nutrients_df[column] = food_nutrients_df[column].apply(append_units, unit=unit)

# Merge the DataFrames on the relevant columns
merged_df = pd.merge(grouped_compounds_foods_df, food_nutrients_df, left_on='name', right_on='food_name', how='inner')

# Display the merged DataFrame
print("Merged DataFrame:")
print(merged_df.info())
print(merged_df.head())

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('data/processed/merged_compounds_nutrients.csv', index=False)
print("Merged data saved to data/processed/merged_compounds_nutrients.csv")