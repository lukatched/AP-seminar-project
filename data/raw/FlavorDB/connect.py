import pandas as pd

# Load the CSV file with combinations
file_path = 'data/processed/updated_combinations_scores_with_nutrient_synergy.csv'
df = pd.read_csv(file_path)

# Print the column names to verify
print("Column names in the CSV file:", df.columns.tolist())

# Check if the required columns exist
required_columns = ['synergy_score', 'pairing_score']
for column in required_columns:
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in the CSV file")

# Find the combination with the highest synergy score and food pairing score
highest_synergy_score = df['synergy_score'].max()
highest_food_pairing_score = df['pairing_score'].max()

# Filter the DataFrame to get the rows with the highest scores
highest_synergy_combinations = df[df['synergy_score'] == highest_synergy_score]
highest_food_pairing_combinations = df[df['pairing_score'] == highest_food_pairing_score]

# Combine the two DataFrames and drop duplicates
highest_score_combinations = pd.concat([highest_synergy_combinations, highest_food_pairing_combinations]).drop_duplicates()

# Save the updated DataFrame to a new CSV file
updated_file_path = 'data/processed/highest_score_combinations.csv'
highest_score_combinations.to_csv(updated_file_path, index=False)
print(f"Updated data saved to {updated_file_path}")