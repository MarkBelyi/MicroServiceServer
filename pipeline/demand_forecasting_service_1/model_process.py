import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

class DemandForecastingService:
    def __init__(self, model_path='random_forest_model_1.pkl'):
        self.model_path = model_path
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def train(self, data: pd.DataFrame):
        X = data[['Season', 'Discount', 'Region', 'Stock_Left']]
        y = data['Quantity_Sold']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        joblib.dump(self.model, self.model_path)
        return {'mse': mse, 'message': 'Demand forecasting model trained and saved.'}

    def predict(self, input_data):
        return self.model.predict([input_data])
