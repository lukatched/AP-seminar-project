import pandas as pd

# Load the CSV files into DataFrames
food_df = pd.read_csv('data/raw/FlavorDB/Food.csv')
compounds_flavor_df = pd.read_csv('data/raw/FlavorDB/CompoundsFlavor.csv')

print("Columns in food_df:", food_df.columns)
print("Columns in compounds_flavor_df:", compounds_flavor_df.columns)

# Merge the DataFrames on the relevant columns
merged_df = pd.merge(compounds_flavor_df, food_df, left_on='flavor_id', right_on='id', how='inner')

# Display the merged DataFrame
print("Merged DataFrame:")
print(merged_df.info())
print(merged_df.head())

# List of columns to remove
columns_to_remove = [
    'citations', 'created_at_x', 'updated_at_x', 'creator_id_x', 'updater_id_x', 
    'source_id', 'source_type', 'id_y', 'name_scientific', 'description', 
    'itis_id', 'wikipedia_id', 'picture_file_name', 'picture_content_type', 
    'picture_file_size', 'picture_updated_at', 'legacy_id', 'food_group', 
    'food_subgroup', 'food_type', 'created_at_y', 'updated_at_y', 'creator_id_y', 
    'updater_id_y', 'export_to_afcdb', 'category', 'ncbi_taxonomy_id', 
    'export_to_foodb', 'public_id'
]

# Remove the specified columns
filtered_df = merged_df.drop(columns=columns_to_remove)

# Display the filtered DataFrame
print("Filtered DataFrame:")
print(filtered_df.info())
print(filtered_df.head())

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('data/processed/matched_compounds_foods_filtered.csv', index=False)
print("Filtered data saved to data/processed/matched_compounds_foods_filtered.csv")