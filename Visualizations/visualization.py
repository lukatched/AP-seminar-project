csv_content = """Step,Description,Next Step
Data Collection,Collecting data from various sources,Data Cleaning
Data Cleaning,Cleaning and preprocessing the collected data,Feature Selection
Feature Selection,Selecting relevant features for the model,Model Training
Model Training,Training the machine learning model,Model Evaluation
Model Evaluation,Evaluating the performance of the model,Visualization
Visualization,Creating visualizations to present the results,Feature Importances for Synergy Score
Feature Importances for Synergy Score,Bar chart showing feature importances for synergy score,Predictions vs. Actual for Synergy Score
Predictions vs. Actual for Synergy Score,Scatter plot showing predictions vs. actual values for synergy score,Residuals for Synergy Score
Residuals for Synergy Score,Histogram showing residuals for synergy score,Distribution of Predictions for Synergy Score
Distribution of Predictions for Synergy Score,Histogram showing distribution of predictions for synergy score,Heatmap for Synergy Score
Heatmap for Synergy Score,Heatmap showing relationship between actual and predicted values for synergy score,Feature Importances for Food Pairing Score
Feature Importances for Food Pairing Score,Bar chart showing feature importances for food pairing score,Predictions vs. Actual for Food Pairing Score
Predictions vs. Actual for Food Pairing Score,Scatter plot showing predictions vs. actual values for food pairing score,Residuals for Food Pairing Score
Residuals for Food Pairing Score,Histogram showing residuals for food pairing score,Distribution of Predictions for Food Pairing Score
Distribution of Predictions for Food Pairing Score,Histogram showing distribution of predictions for food pairing score,Heatmap for Food Pairing Score
Heatmap for Food Pairing Score,Heatmap showing relationship between actual and predicted values for food pairing score,
"""

with open('c:/Users/Luka Anthony/OneDrive/Documents/Food Project/data/processed/process_diagram.csv', 'w') as file:
    file.write(csv_content)