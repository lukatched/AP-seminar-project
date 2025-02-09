<<<<<<< HEAD
import csv
import shutil
import os
from difflib import SequenceMatcher

# filepath: /c:/Users/Luka Anthony/OneDrive/Documents/Food Project/data/raw/FlavorDB/remove.py

def normalize_food_name(name):
    return name.lower().strip()

def backup_file(file_path):
    backup_path = file_path + '.bak'
    shutil.copy(file_path, backup_path)
    print(f"Backup created at {backup_path}")
    return backup_path

def restore_file(file_path, backup_path):
    shutil.copy(backup_path, file_path)
    os.remove(backup_path)
    print(f"File restored from {backup_path}")

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def rename_and_filter_foods(file_path, common_food_names, similarity_threshold=0.8):
    updated_rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        updated_rows.append(header)
        for row in reader:
            original_name = normalize_food_name(row[1])
            best_match = None
            highest_similarity = 0
            for common_name in common_food_names:
                similarity = similar(original_name, common_name)
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match = common_name
            if highest_similarity >= similarity_threshold:
                row[1] = best_match  # Rename the food name to the best match
                print(f"Renamed '{original_name}' to '{best_match}' with similarity {highest_similarity:.2f}")
                updated_rows.append(row)

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)  # Write only the updated rows to the file
        print(f"File written to {file_path} with renamed food names.")

# List of common food names
common_food_names = [
    "apple", "banana", "carrot", "broccoli", "spinach", "tomato", "potato", "onion", "garlic", "pepper",
    "chicken", "beef", "pork", "fish", "rice", "bread", "milk", "cheese", "yogurt", "egg",
    "orange", "grape", "strawberry", "blueberry", "raspberry", "watermelon", "melon", "lettuce", "cucumber", "zucchini",
    "almond", "walnut", "peanut", "cashew", "hazelnut", "pistachio", "sunflower seed", "pumpkin seed", "chia seed", "flaxseed",
    "oatmeal", "pasta", "quinoa", "barley", "corn", "peas", "beans", "lentils", "chickpeas", "soybean",
    "butter", "margarine", "olive oil", "coconut oil", "canola oil", "avocado", "mango", "pineapple", "kiwi", "pear",
    "plum", "peach", "apricot", "cherry", "fig", "date", "raisin", "cranberry", "blackberry", "pomegranate",
    "sweet potato", "beet", "radish", "turnip", "parsnip", "celery", "fennel", "leek", "kale", "collard greens",
    "brussels sprouts", "cauliflower", "cabbage", "artichoke", "asparagus", "mushroom", "bell pepper", "jalapeno", "chili pepper", "ginger",
    "turmeric", "cinnamon", "nutmeg", "clove", "cardamom", "coriander", "cumin", "dill", "fennel seed", "mustard seed",
    "parsley", "basil", "oregano", "thyme", "rosemary", "sage", "mint", "cilantro", "chive", "tarragon",
    "grapefruit", "lemon", "lime", "papaya", "passion fruit", "peanut butter", "peppermint", "pistachio", "plum", "pomegranate",
    "popcorn", "potato chips", "pumpkin", "radish", "raspberry", "red cabbage", "red onion", "red pepper", "rhubarb", "rice cakes",
    "romaine lettuce", "rosemary", "sage", "salmon", "sardines", "scallions", "shallots", "shrimp", "snap peas", "snow peas",
    "soy sauce", "spaghetti", "spinach", "squash", "strawberry", "sunflower seeds", "sweet corn", "sweet potato", "tangerine", "thyme",
    "tofu", "tomato", "tuna", "turkey", "vanilla", "walnut", "watercress", "watermelon", "wheat bread", "white bread",
    "white rice", "whole wheat bread", "wild rice", "yogurt", "zucchini"
]

# Backup the original file
backup_path = backup_file('data/raw/FlavorDB/Food.csv')

# Rename and filter the foods in the CSV file
rename_and_filter_foods('data/raw/FlavorDB/Food.csv', common_food_names)

# Restore the original file if needed
# restore_file('/c:/Users/Luka Anthony/OneDrive/Documents/Food Project/data/raw/FlavorDB/Food.csv', backup_path)
=======
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
>>>>>>> 26ba0b8a089504646eb23566857d8440ecdbd85b
