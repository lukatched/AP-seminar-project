import pandas as pd
import requests


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
nutritionix_app_id = '81bcc29f'
nutritionix_app_key = '64a2364aa967fdf9e38dec6d157cbbb4'

# Define the endpoint for the API
def get_nutritionix_data(query):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
<<<<<<< HEAD
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
=======
        "Content-Type": "application/json",
        "x-app-id": nutritionix_app_id,
        "x-app-key": nutritionix_app_key
}
    body = {
        "query": query
}
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        #tuple-data structure has multiple data pieces, returns response
        return(response.json())
    else:
        print(f"Error handling query;{query}: {response.status_code}")

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
>>>>>>> f6d8d98fc0db30d6ad1b8b99f342342e7167903a

           
queries = ["apple", "banana", "orange", "grape", "strawberry"]
get_bulk_nutritionix_data(queries).to_csv("bulk_nutritionix_data.csv", index=False)

#next snake case the columns


 