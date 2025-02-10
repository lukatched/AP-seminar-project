import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure the directory exists
output_dir = 'data/processed'
os.makedirs(output_dir, exist_ok=True)

# Load the CSV file with nutrient content into a DataFrame
nutrient_df = pd.read_csv(os.path.join(output_dir, 'merged_compounds_nutrients.csv'))

# Select the relevant columns for nutrients
nutrients_of_interest = ['324', '301', '303', '305', '309', '307', '430', '417', '404', '405']

# Convert nutrient columns to numeric values (removing units like 'mg', 'µg')
for nutrient in nutrients_of_interest:
    nutrient_df[nutrient] = nutrient_df[nutrient].str.replace('mg', '').str.replace('µg', '').astype(float)

# Pivot the DataFrame to have foods as rows and nutrients as columns
pivot_df = nutrient_df.pivot_table(index='food_name', values=nutrients_of_interest, aggfunc='mean').fillna(0)

# Create individual bar charts for each nutrient
for nutrient in nutrients_of_interest:
    plt.figure(figsize=(14, 10))
    pivot_df[nutrient].plot(kind='bar', color='skyblue')
    plt.xlabel('Food', fontsize=14)
    plt.ylabel('Amount', fontsize=14)
    plt.title(f'Nutrient {nutrient} Content of Each Food', fontsize=16)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    # Save the plot as an image file
    output_file = os.path.join(output_dir, f'nutrient_{nutrient}_content.png')
    plt.savefig(output_file, bbox_inches='tight')
    plt.show()