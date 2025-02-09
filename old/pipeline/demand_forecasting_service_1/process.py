import pickle
import pandas as pd

class DemandForecastingService:
    def __init__(self):
        self.model_path = 'pipeline/1_demand_forecasting_service/random_forest_model_1.pkl'

    def load_model(self):
        with open(self.model_path, 'rb') as f:
            return pickle.load(f)

    def forecast(self, data):
        """
        Прогноз спроса.
        :param data: DataFrame с характеристиками продуктов.
        :return: DataFrame с добавленным прогнозом спроса.
        """
        model = self.load_model()
        features = data[['Region', 'Season', 'Holiday', 'Discount', 'Quantity_Sold']]
        features_encoded = pd.get_dummies(features, columns=['Region', 'Season'])
        predictions = model.predict(features_encoded)
        data['Predicted_Demand'] = predictions
        return data
