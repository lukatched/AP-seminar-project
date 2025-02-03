import csv
import shutil
import os
import requests

def get_nutritionix_food_names():
    headers = {
        "Content-Type": "application/json",
        "x-app-id": os.getenv("NUTRITIONIX_APP_ID"),
        "x-app-key": os.getenv("NUTRITIONIX_APP_KEY")
    }
    url = "https://trackapi.nutritionix.com/v2/search/instant?query="
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        food_names = [item['food_name'].lower() for item in data['common']]
        print(f"Retrieved {len(food_names)} food names from Nutritionix API.")
        return food_names
    else:
        print(f"Error fetching food names from Nutritionix: {response.status_code}")
        return []

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

def filter_and_rename_foods(file_path, nutritionix_food_names):
    filtered_rows = []
    removed_rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        header.append('nutritionix_name')  # Add a new column for Nutritionix names
        filtered_rows.append(header)
        for row in reader:
            original_name = normalize_food_name(row[1])
            if original_name in nutritionix_food_names:
                row.append(original_name)  # Add the Nutritionix name to the row
                filtered_rows.append(row)
                print(f"Row added: {row}")
            else:
                removed_rows.append(row)
                print(f"Row removed: {row}")
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(filtered_rows)  # Write only the filtered rows to the file
        print(f"File written to {file_path} with {len(filtered_rows)} filtered rows and {len(removed_rows)} removed rows")

# Backup the original file
backup_path = backup_file('data/raw/FlavorDB/Food.csv')

# Retrieve the list of food names from the Nutritionix API
nutritionix_food_names = get_nutritionix_food_names()

# Filter and rename the foods in the CSV file
filter_and_rename_foods('data/raw/FlavorDB/Food.csv', nutritionix_food_names)

# Restore the original file if needed
# restore_file('/c:/Users/Luka Anthony/OneDrive/Documents/Food Project/data/raw/FlavorDB/Food.csv', backup_path)