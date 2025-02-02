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
    'Vitamin D': {'Calcium': 0.25},  # Vitamin D increases Calcium absorption by 25%
    'Calcium': {'Vitamin D': 0.20},  # Calcium increases Vitamin D absorption by 20%
    'Iron': {'Vitamin C': 0.30}      # Iron absorption is increased by 30% with Vitamin C
}

inhibitory_nutrients = {
    'Calcium': {'Iron': -0.10},  # Calcium inhibits Iron absorption by 10%
    'Iron': {'Calcium': -0.10}   # Iron inhibits Calcium absorption by 10%
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

def calculate_nutrient_synergy_score(nutrients):
    synergy_score = 0
    for nutrient in nutrients:
        if nutrient['attr_id'] == 324:  # Vitamin D
            synergy_score += nutrient['value'] * 1.5  # Example weight
        elif nutrient['attr_id'] == 301:  # Calcium
            synergy_score += nutrient['value'] * 1.2  # Example weight
        elif nutrient['attr_id'] == 303:  # Iron
            synergy_score += nutrient['value'] * 1.3  # Example weight
    return synergy_score

merged_df['nutrient_synergy_score'] = merged_df['full_nutrients'].apply(calculate_nutrient_synergy_score)

def calculate_palatability_score(food_name, flavor_data):
    shared_compounds = flavor_data[flavor_data['flavor_name'] == food_name]['compound_id'].nunique()
    return shared_compounds

merged_df['palatability_score'] = merged_df['food_name'].apply(lambda x: calculate_palatability_score(x, dataframes['compounds_flavor']))

def filter_inhibitory_interactions(nutrients):
    for nutrient in nutrients:
        if nutrient['attr_id'] in inhibitory_nutrients:
            for inhibitory in inhibitory_nutrients[nutrient['attr_id']]:
                if any(n['attr_id'] == inhibitory for n in nutrients):
                    return False
    return True

# Calculate scores and filter data
merged_df = merged_df[merged_df['full_nutrients'].apply(filter_inhibitory_interactions)]

# Sort by scores
merged_df = merged_df.sort_values(by=['nutrient_synergy_score', 'palatability_score'], ascending=False)

# Display the top combinations
print(merged_df.head(10))