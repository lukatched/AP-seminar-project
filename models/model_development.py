import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('data/processed/merged_scores_with_nutrients.csv')

# Debug print statement to check the data
print("Data loaded from merged_scores_with_nutrients.csv:")
print(data.head())

# Define features for synergy score model (focus on Calcium, Iron, and Vitamin D)
synergy_features = ['pairing_score', '324', '301', '303']  # Assuming '324' is Calcium, '301' is Iron, '303' is Vitamin D
synergy_target = 'synergy_score'

# Define features for food pairing score model (focus on flavor compounds)
pairing_features = ['324', '301', '303']  # Assuming '324' is Calcium, '301' is Iron, '303' is Vitamin D
pairing_target = 'pairing_score'

# Function to train and evaluate a model
def train_and_evaluate_model(features, target, data):
    X = data[features]
    y = data[target]

    # Debug print statement to check the features and target variable
    print(f"Features and target variable for {target}:")
    print(X.head())
    print(y.head())

    # Check for any constant columns in the features
    constant_columns = [col for col in X.columns if X[col].nunique() == 1]
    if constant_columns:
        print(f"Constant columns found: {constant_columns}")
        X = X.drop(columns=constant_columns)

    # Check the number of samples in the dataset
    print(f"Number of samples in the dataset: {X.shape[0]}")

    # Adjust the test_size parameter if necessary
    test_size = 0.2
    if X.shape[0] < 10:  # If there are less than 10 samples, use a smaller test size
        test_size = 0.1
    if X.shape[0] < 2:  # If there are less than 2 samples, use the entire dataset for training
        test_size = 0.0

    # Split the data into training and testing sets
    if test_size > 0:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    else:
        X_train, X_test, y_train, y_test = X, X, y, y

    # Check the number of samples in the training and testing sets
    print(f"Number of samples in the training set: {X_train.shape[0]}")
    print(f"Number of samples in the testing set: {X_test.shape[0]}")

    # Train the Random Forest Regressor with smaller parameters for small datasets
    model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # Debug print statement to check the model training
    print(f"Model trained for {target}. Feature importances:")
    print(model.feature_importances_)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Debug print statement to check the predictions
    print(f"Predictions on the test set for {target}:")
    print(predictions)

    # Evaluate the model
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f'MSE for {target}: {mse}, R2: {r2}')

    # Output the results for visualization in Lucidchart
    results = pd.DataFrame({
        'Actual': y_test,
        'Predicted': predictions
    })
    results.to_csv(f'data/processed/prediction_results_{target}.csv', index=False)

    print(f"Prediction results for {target} saved to data/processed/prediction_results_{target}.csv")

    # Generate heatmap data for Lucidchart
    heatmap_data = pd.pivot_table(results, values='Predicted', index='Actual', columns='Predicted', aggfunc=np.mean)
    heatmap_data.to_csv(f'data/processed/heatmap_data_{target}.csv')

    print(f"Heatmap data for {target} saved to data/processed/heatmap_data_{target}.csv")

    # Plot feature importances
    plt.figure(figsize=(10, 6))
    feature_importances = pd.Series(model.feature_importances_, index=X.columns)
    feature_importances.nlargest(10).plot(kind='barh')
    plt.title(f'Feature Importances for {target}')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.savefig(f'data/processed/feature_importances_{target}.png')
    plt.show()

    # Plot predictions vs actual values
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Actual', y='Predicted', data=results)
    plt.plot([results['Actual'].min(), results['Actual'].max()], [results['Actual'].min(), results['Actual'].max()], 'r--')
    plt.title(f'Predictions vs Actual for {target}')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.savefig(f'data/processed/predictions_vs_actual_{target}.png')
    plt.show()

    # Plot residuals
    residuals = y_test - predictions
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, kde=True)
    plt.title(f'Residuals for {target}')
    plt.xlabel('Residual')
    plt.ylabel('Frequency')
    plt.savefig(f'data/processed/residuals_{target}.png')
    plt.show()

    # Plot distribution of predictions
    plt.figure(figsize=(10, 6))
    sns.histplot(predictions, kde=True)
    plt.title(f'Distribution of Predictions for {target}')
    plt.xlabel('Predicted Value')
    plt.ylabel('Frequency')
    plt.savefig(f'data/processed/predictions_distribution_{target}.png')
    plt.show()

# Train and evaluate the model for synergy score
train_and_evaluate_model(synergy_features, synergy_target, data)

# Train and evaluate the model for food pairing score
train_and_evaluate_model(pairing_features, pairing_target, data)