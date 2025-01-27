import pandas as pd
from flask import Flask, jsonify
import requests

app = Flask(__name__)
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
nutritionix_app_key = '6b3c2f5b0c5d2d6e1b6b0d6f7e1d5b4f'

# Define the endpoint for the API
def get_nutritionix_data(query):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        'x-app-id': nutritionix_app_id,
        'x-app-key': nutritionix_app_key,
        "Content-Type": 'application/json'
    }
    response = requests.post(url, headers=headers, json={"query": query})
    return response.json()

# function to defind endpoint of APi as well as fetching the data and getting it ready to put into a dataframe
def get_bulk_nutritionix_data(queries):
    all_nutrition_data = []
    for query in queries:
        nutrition_data = get_nutritionix_data
        all_nutrition_data.extend(nutrition_data)
    return all_nutrition_data
    
    response = requests.post(url + request, headers=headers, json=query)
    return response.json()


def get_combined_data():
    #combining all the data from fooDB into one dataframe to simplify the data
    combined_df= pd.concat([dataframes['compounds_enzyme'], dataframes['compounds_flavor'], dataframes['enzyme'], dataframes['enzyme_synonym'], dataframes['flavor'], dataframes['food']])
    #example query
    nutrition_query = "apple" #example query, create function get bulk nutrition data here 
    nutrition_data = get_nutritionix_data(nutrition_query)
    #nutritionix data normalized to dataframe
    nutrition_df = pd.json_normalize(nutrition_data)
    #combines both dataframes into one
    final_combined_df = pd.concat([combined_df, nutrition_df], ignore_index=True)
    return final_combined_df

df= get_combined_data()


df.isnull().sum()

# displays numerical information of data in normal notation rather than scientific notation
with pd.option_context('display.float_format', '{:f}'.format):
    print(df.describe())

#next snake case the columns


