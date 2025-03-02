import csv
import pandas as pd
import requests
import os
import matplotlib.pyplot as plt

file_paths = {
    'compounds_enzyme': 'data/raw/FlavorDB/CompoundsEnzyme.csv',
    'compounds_flavor': 'data/raw/FlavorDB/CompoundsFlavor.csv',
    'enzyme': 'data/raw/FlavorDB/Enzyme.csv',
    'enzyme_synonym': 'data/raw/FlavorDB/EnzymeSynonym.csv',
    'flavor': 'data/raw/FlavorDB/Flavor.csv',
    'food': 'data/raw/FlavorDB/Food.csv'
 }

# Load data into dataframes to compress into a manageable piece
dataframes = {name: pd.read_csv(path) for name, path in file_paths.items()}


# giving variables to the api information simplifies the code
nutritionix_app_id = '4d507ef0'
nutritionix_app_key = '759e42e980f29a3319279026d2f13c37'

# Define the endpoint for the API
def get_nutritionix_data(query):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        'x-app-id': nutritionix_app_id,
        'x-app-key': nutritionix_app_key,
        "Content-Type": 'application/json'
    }
    body = {
        "query": query,
        }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        #tuple-data structure has multiple data pieces, returns response
        return(response.json())
    else:
        print(f"Error handling query;{query}: {response.status_code}")


def normalize_food_name(name):
    return name.lower().strip()

def get_food_names():
    food_names = []
    with open("data/raw/FlavorDB/Food.csv", mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) > 1:  # Ensure there are at least two elements in the row
                food_names.append(row[1])  # Append the second element (food name) to the list
    return food_names



# function to defind endpoint of APi as well as fetching the data and getting it ready to put into a dataframe
def get_bulk_nutritionix_data(queries):
    responses = []
    for query in queries: 
        data = get_nutritionix_data(query)
        #appends data to apporpriate query
        responses.append({"query":query,"response":data})
    df=pd.DataFrame(responses)
    normalized_data = pd.json_normalize(df["response"], record_path="foods")
# Select only the `food_name` and `full_nutrients` columns
    final_df = normalized_data[["food_name", "full_nutrients"]]
    return(final_df)



# main starts here
food_names = get_food_names()
print(food_names)

bulk_data = get_bulk_nutritionix_data(food_names)
nutrition_df = pd.json_normalize(bulk_data, record_path=["foods"], meta=["food_name"])

filtered_df = nutrition_df[nutrition_df
            (nutrition_df['full_nutrients'].apply(lambda x: any(nutrient['attr_id']in [301, 303, 309, 304, 401, 305, 430, 307, 324, 262, 221, 232]for nutrient in x)))
            ]
