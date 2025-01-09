import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def train_model(data):
    X = data[['feature1', 'feature2']]  # Replace with actual feature names
    y = data['target']  # Replace with actual target variable
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f'MSE: {mse}, R2: {r2}')

if __name__ == "__main__":
    data = pd.read_csv('data/processed/merged_data.csv')
    train_model(data)
