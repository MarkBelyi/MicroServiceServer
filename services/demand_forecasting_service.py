# services/demand_forecasting_service.py

import numpy as np
from services.models.demand_forecasting_model import build_demand_forecasting_model

class DemandForecastingService:
    def __init__(self):
        # Допустим, модель принимает последовательность с 1 временным шагом и 1 признаком
        self.model = build_demand_forecasting_model(input_shape=(1, 1))

    def forecast(self, data):
        # Из колонки 'Quantity_Sold' формируем входной массив для модели
        X = data['Quantity_Sold'].values.reshape(-1, 1, 1)
        predicted = self.model.predict(X)
        data['Predicted_Demand'] = predicted.flatten()
        return data
