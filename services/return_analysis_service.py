# services/return_analysis_service.py

import numpy as np
from services.models.return_analysis_model import build_return_analysis_model

class ReturnAnalysisService:
    def __init__(self):
        # Используем один признак – отношение возвратов к количеству продаж
        self.model = build_return_analysis_model(input_shape=(1, 1))

    def analyze(self, data, optimized_procurement):
        ratio = data.apply(lambda row: row['Returns'] / row['Quantity_Sold'] if row['Quantity_Sold'] > 0 else 0, axis=1)
        X = ratio.values.reshape(-1, 1, 1)
        predicted = self.model.predict(X)
        data['Return_Rate'] = predicted.flatten() * 100  # в процентах
        return data
