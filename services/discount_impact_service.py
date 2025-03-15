# services/discount_impact_service.py

import numpy as np
from services.models.discount_impact_model import build_discount_impact_model


class DiscountImpactService:
    def __init__(self):
        # Модель принимает булевый признак (Holiday) в числовом виде
        self.model = build_discount_impact_model(input_dim=1)

    def analyze(self, data, regional_analysis):
        # Преобразуем булевое значение в число: True -> 1, False -> 0
        data['Holiday_Numeric'] = data['Holiday'].apply(lambda x: 1 if x else 0)
        X = data['Holiday_Numeric'].values.reshape(-1, 1)
        predicted = self.model.predict(X)
        # Корректировка прогноза спроса; например, Final_Demand = Predicted_Demand * (1 + prediction)
        data['Final_Demand'] = data['Predicted_Demand'] * (1 + predicted.flatten())
        return data
