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

food_names = dataframes['food']['name'].unique().tolist()

# giving variables to the api information simplifies the code
nutritionix_app_id = '81bcc29f'
nutritionix_app_key = '64a2364aa967fdf9e38dec6d157cbbb4'

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

bulk_data = get_bulk_nutritionix_data('food_name')
nutrition_df = pd.json_normalize(bulk_data["full_nutrients"])

filtered_df = nutrition_df[nutrition_df
            (nutrition_df['full_nutrients'].apply(lambda x: any(nutrient['attr_id']in [324,301,303]for nutrient in x)))
            ]

merged_df=pd.merge(filtered_df, dataframes ['food'], left_on='food_name', right_on='name', how='inner')


synergistic_nutrients = {
    'Vitamin D': ['Calcium'],
    'Calcium': ['Vitamin D'],
    'Iron': ['Vitamin C']  # Example of a synergistic interaction
}

inhibitory_nutrients = {
    'Calcium': ['Iron'],  # Example of an inhibitory interaction
    'Iron': ['Calcium']
}
 

def calculate_nutrient_absorption_score(nutrients):
    score = 0
    for nutrient in nutrients:
        if nutrient['attr_id'] in [324, 301, 303]:  # Vitamin D, Calcium, Iron
            score += nutrient['value']
    return score

def calculate_palatability_score(food_name, flavor_data):
    # Example: Count the number of shared aroma compounds
    shared_compounds = flavor_data[flavor_data['flavor_name'] == food_name]['compound_id'].nunique()
    return shared_compounds

def filter_inhibitory_interactions(nutrients):
    for nutrient in nutrients:
        if nutrient['attr_id'] in inhibitory_nutrients:
            for inhibitory in inhibitory_nutrients[nutrient['attr_id']]:
                if any(n['attr_id'] == inhibitory for n in nutrients):
                    return False
    return True