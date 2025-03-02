import pandas as pd
from itertools import combinations

# Define the nutrients of interest
nutrient_ids = ['Vitamin D', 'Calcium', 'Magnesium', 'Phosphorus', 'Vitamin K', 'Sodium', 'Iron', 'Zinc', 'Caffeine']

# Generate all possible combinations of the specified nutrients
all_combinations = []
for r in range(1, len(nutrient_ids) + 1):
    combinations_r = combinations(nutrient_ids, r)
    all_combinations.extend(combinations_r)

# Define the criteria points
criteria_points = {
    'strength_of_evidence': 3,
    'magnitude': 2,
    'consistent_across_population': 2,
    'mechanism_of_action': 3,
    'clinical_relevance': 3,
    'reproducibility': 3
}

# Define the interactions with criteria points
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
        },
        'Magnesium': {
            'strength_of_evidence': 3,
            'magnitude': 2,
            'consistent_across_population': 2,
            'mechanism_of_action': 3,
            'clinical_relevance': 3,
            'reproducibility': 2
        },
        'Phosphorus': {
            'strength_of_evidence': 3,
            'magnitude': 2,
            'consistent_across_population': 1,
            'mechanism_of_action': 3,
            'clinical_relevance': 3,
            'reproducibility': 1
        },
        'Vitamin K': {
            'strength_of_evidence': 3,
            'magnitude': 3,
            'consistent_across_population': 3,
            'mechanism_of_action': 3,
            'clinical_relevance': 3,
            'reproducibility': 2
        },
        'Sodium': {
            'strength_of_evidence': -3,
            'magnitude': -3,
            'consistent_across_population': -3,
            'mechanism_of_action': -3,
            'clinical_relevance': -3,
            'reproducibility': -3
        },
        'Iron': {
            'strength_of_evidence': -3,
            'magnitude': -3,
            'consistent_across_population': -3,
            'mechanism_of_action': -3,
            'clinical_relevance': -3,
            'reproducibility': -3
        },
        'Zinc': {
            'strength_of_evidence': -3,
            'magnitude': -3,
            'consistent_across_population': -3,
            'mechanism_of_action': -3,
            'clinical_relevance': -3,
            'reproducibility': -3
        },
        'Caffeine': {
            'strength_of_evidence': -3,
            'magnitude': -3,
            'consistent_across_population': -3,
            'mechanism_of_action': -3,
            'clinical_relevance': -3,
            'reproducibility': -3
        }
    },
    'Magnesium': {
        'Calcium': {
            'strength_of_evidence': 3,
            'magnitude': 2,
            'consistent_across_population': 2,
            'mechanism_of_action': 3,
            'clinical_relevance': 3,
            'reproducibility': 2
        }
    },
    'Phosphorus': {
        'Calcium': {
            'strength_of_evidence': 3,
            'magnitude': 2,
            'consistent_across_population': 1,
            'mechanism_of_action': 3,
            'clinical_relevance': 3,
            'reproducibility': 1
        }
    },
    'Vitamin K': {
        'Calcium': {
            'strength_of_evidence': 3,
            'magnitude': 3,
            'consistent_across_population': 3,
            'mechanism_of_action': 3,
            'clinical_relevance': 3,
            'reproducibility': 2
        }
    },
    'Sodium': {
        'Calcium': {
            'strength_of_evidence': -3,
            'magnitude': -3,
            'consistent_across_population': -3,
            'mechanism_of_action': -3,
            'clinical_relevance': -3,
            'reproducibility': -3
        }
    },
    'Iron': {
        'Calcium': {
            'strength_of_evidence': -3,
            'magnitude': -3,
            'consistent_across_population': -3,
            'mechanism_of_action': -3,
            'clinical_relevance': -3,
            'reproducibility': -3
        }
    },
    'Zinc': {
        'Calcium': {
            'strength_of_evidence': -3,
            'magnitude': -3,
            'consistent_across_population': -3,
            'mechanism_of_action': -3,
            'clinical_relevance': -3,
            'reproducibility': -3
        }
    },
    'Caffeine': {
        'Calcium': {
            'strength_of_evidence': -3,
            'magnitude': -3,
            'consistent_across_population': -3,
            'mechanism_of_action': -3,
            'clinical_relevance': -3,
            'reproducibility': -3
        }
    }
}

def calculate_interaction_score(interaction):
    total_points = 18  # The maximum possible points
    obtained_points = sum(interaction.values())
    score = (obtained_points / total_points * 2) - 1
    # Ensure the score is within the range of -1 to 1
    score = max(min(score, 1), -1)
    return score

def calculate_nutrient_synergy_score(nutrients):
    nutrient_score = 0
    for nutrient in nutrients:
        if nutrient in interactions:
            for interacting_nutrient, interaction in interactions[nutrient].items():
                if interacting_nutrient in nutrients:
                    score = calculate_interaction_score(interaction)
                    nutrient_score += score
    return nutrient_score

# Calculate the synergy score for each combination
synergy_scores = []
for combination in all_combinations:
    score = calculate_nutrient_synergy_score(combination)
    synergy_scores.append({
        'combination': combination,
        'synergy_score': score
    })

# Create a DataFrame from the results
synergy_df = pd.DataFrame(synergy_scores)

# Save the results to a CSV file
output_csv_path = '/Users/lukaanthony/Documents/GitHub/AP-seminar-project/data/raw/FlavorDB/Nutrient_Synergy_Scores.csv'
synergy_df.to_csv(output_csv_path, index=False)

print("Nutrient synergy scores saved successfully.")