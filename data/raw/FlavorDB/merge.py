import pandas as pd
from itertools import combinations

# Load the datasets
grouped_df = pd.read_csv('data/processed/grouped.csv')
pairing_scores_df = pd.read_csv('data/processed/food_pairing_scores.csv')
synergy_scores_df = pd.read_csv('data/raw/FlavorDB/Nutrient_Synergy_Scores.csv')
nutrient_data = pd.read_csv('data/raw/FlavorDB/Food_Nutrients.csv')

# Debug print statements to check the contents of the loaded DataFrames
print("Grouped DataFrame:")
print(grouped_df.head())
print("Pairing Scores DataFrame:")
print(pairing_scores_df.head())
print("Synergy Scores DataFrame:")
print(synergy_scores_df.head())
print("Nutrient Data DataFrame:")
print(nutrient_data.head())

# Function to calculate the total nutrient amounts for each food combination
def calculate_nutrient_amounts(foods, nutrient_data):
    nutrient_columns = ['324', '301', '303', '305', '309', '307', '430', '417', '404', '405']
    total_nutrients = {nutrient: 0.0 for nutrient in nutrient_columns}
    
    for food in foods:
        food_data = nutrient_data[nutrient_data['food_name'] == food]
        if not food_data.empty:
            for nutrient in nutrient_columns:
                amount_str = food_data[nutrient].values[0]
                amount = float(amount_str)
                total_nutrients[nutrient] += amount
    
    return total_nutrients

# Add nutrient amounts to the merged dataset
nutrient_columns = ['324', '301', '303', '305', '309', '307', '430', '417', '404', '405']

# Create a new DataFrame to store the results
results_df = pd.DataFrame(columns=['combination', 'pairing_score', 'synergy_score'] + nutrient_columns)

for idx, row in pairing_scores_df.iterrows():
    foods = eval(row['foods'])
    pairing_score = row['pairing_score']
    
    # Find the corresponding synergy score
    synergy_score_row = synergy_scores_df[synergy_scores_df['combination'] == str(foods)]
    if not synergy_score_row.empty:
        synergy_score = synergy_score_row['synergy_score'].values[0]
    else:
        synergy_score = 0.0
    
    print(f"Processing combination: {foods}")  # Debug print
    total_nutrients = calculate_nutrient_amounts(foods, nutrient_data)
    print(f"Total nutrients for combination {foods}: {total_nutrients}")  # Debug print
    
    # Create a new row with the combination, pairing score, synergy score, and nutrient amounts
    new_row = pd.DataFrame([{'combination': str(foods), 'pairing_score': pairing_score, 'synergy_score': synergy_score, **total_nutrients}])
    
    # Append the new row to the results DataFrame using pd.concat
    results_df = pd.concat([results_df, new_row], ignore_index=True)

# Display the results DataFrame
print("Results DataFrame with Food Pairing, Nutrient Synergy Scores, and Nutrient Amounts:")
print(results_df.info())
print(results_df.head())

# Save the results DataFrame to a new CSV file
results_df.to_csv('data/processed/merged_scores_with_nutrients.csv', index=False)
print("Merged data with food pairing, nutrient synergy scores, and nutrient amounts saved to data/processed/merged_scores_with_nutrients.csv")