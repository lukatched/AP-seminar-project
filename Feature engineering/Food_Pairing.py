import pandas as pd
from itertools import combinations

# Load the CSV file into a DataFrame
grouped_df = pd.read_csv('data/processed/grouped.csv')

# Function to calculate the food pairing score based on shared flavor compounds
def calculate_food_pairing_score(foods):
    all_compounds = [set(food['compound_ids'].split(',')) for food in foods]
    shared_compounds = set.intersection(*all_compounds)
    total_unique_compounds = set.union(*all_compounds)
    score = len(shared_compounds) / len(total_unique_compounds) if total_unique_compounds else 0
    return score

# Function to generate all possible combinations of foods
def generate_combinations(df, max_combination_size):
    all_combinations = []
    for size in range(2, max_combination_size + 1):
        all_combinations.extend(combinations(df.iterrows(), size))
    return all_combinations

# Define the maximum combination size
max_combination_size = 3  # You can change this value as needed

# Generate all possible combinations of foods
food_combinations = generate_combinations(grouped_df, max_combination_size)

# Calculate the food pairing scores for each combination
pairing_scores = []
for combination in food_combinations:
    foods = [food for idx, food in combination]
    score = calculate_food_pairing_score(foods)
    pairing_scores.append({
        'foods': [food['name'] for food in foods],
        'flavor_ids': [food['flavor_id'] for food in foods],
        'compound_ids': [food['compound_ids'] for food in foods],
        'pairing_score': score
    })

# Create a DataFrame with the pairing scores
pairing_scores_df = pd.DataFrame(pairing_scores)

# Display the DataFrame with pairing scores
print("DataFrame with Food Pairing Scores:")
print(pairing_scores_df.info())
print(pairing_scores_df.head())

# Save the DataFrame with pairing scores to a new CSV file
pairing_scores_df.to_csv('data/processed/food_pairing_scores.csv', index=False)
print("Data with food pairing scores saved to data/processed/food_pairing_scores.csv")