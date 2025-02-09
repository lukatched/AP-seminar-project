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

bulk_data = get_bulk_nutritionix_data(food_names)
nutrition_df = pd.json_normalize(bulk_data)

nutrient_ids = [324, 301, 303, 305, 309, 307, 430, 417, 404, 405]  # Add the nutrient IDs for phosphorus, magnesium, etc.
filtered_df = nutrition_df[
    nutrition_df['full_nutrients'].apply(lambda x: any(nutrient['attr_id'] in nutrient_ids for nutrient in x))
]
merged_df=pd.merge(filtered_df, dataframes['food'], left_on='food_name', right_on='name', how='inner')


dataframes['food']['name'] = dataframes['food']['name'].str.lower()
merged_df['food_name'] = merged_df['food_name'].str.lower()



# scoring framework starts here
criteria_points = {
    'strength of evidence': 3,
    'magnitude':2,
    'consistent_across_population': 2,
    'mechanism_of_action':3,
    'clinical_relevance':3,
    'reporducibility':2
}

interactions = {
    'Vitamin D': {
        'Calcium': {
            'strength_of_evidence': 3,
            'magnitude': 2,
            'consistent_across_population': 2,
            'mechanism_of_action': 3,
            'clinical_relevance': 3,
            'reproducibility': 3
        }
    },
    'Calcium': {
        'Vitamin D': {
            'strength_of_evidence': 3,
            'magnitude': 2,
            'consistent_across_population': 2,
            'mechanism_of_action': 3,
            'clinical_relevance': 3,
            'reproducibility': 3
        }
    },
    'Iron': {
        'Vitamin C': {
            'strength_of_evidence': 3,
            'magnitude': 2,
            'consistent_across_population': 2,
            'mechanism_of_action': 3,
            'clinical_relevance': 3,
            'reproducibility': 3
        }
    }
}

def calculate_interaction_score(interaction): 
    total_points = sum(criteria_points.values())
    obtained_points = sum(interaction.values())
    score = (obtained_points / total_points) * 2
    return score

def calculate_nutrient_score(nutrients):
    nutrient_score = 0
    for nutrient in nutrients:
        attr_id = nutrient['attr_id']
        value = nutrient['value']
        
        # Check for interactions
        if attr_id in interactions:
            for interacting_nutrient, interaction in interactions[attr_id].items():
                if any(n['attr_id'] == interacting_nutrient for n in nutrients):
                    score = calculate_interaction_score(interaction)
                    nutrient_score += value * score
    
    return nutrient_score

def calculate_palatability_score(food_name, flavor_data):
    shared_compounds = flavor_data[flavor_data['flavor_name'] == food_name]['compound_id'].nunique()
    return shared_compounds

# Calculate scores and filter data
merged_df['nutrient_score'] = merged_df['full_nutrients'].apply(calculate_nutrient_score)
merged_df['palatability_score'] = merged_df['food_name'].apply(lambda x: calculate_palatability_score(x, dataframes['compounds_flavor']))

merged_df = merged_df.sort_values(by=['nutrient_score', 'palatability_score'], ascending=False)

# Display the top combinations
print(merged_df[['food_name', 'nutrient_score', 'palatability_score']].head(10))

