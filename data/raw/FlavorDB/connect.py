import pandas as pd

# Load the CSV files into DataFrames
food_df = pd.read_csv('data/raw/FlavorDB/Food.csv')
compounds_flavor_df = pd.read_csv('data/raw/FlavorDB/CompoundsFlavor.csv')

# Merge the DataFrames on the relevant columns
merged_df = pd.merge(food_df, compounds_flavor_df, left_on='id', right_on='flavor_id', how='inner')

# Display the merged DataFrame
print("Merged DataFrame:")
print(merged_df.info())
print(merged_df.head())