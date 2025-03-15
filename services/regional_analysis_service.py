# services/regional_analysis_service.py

import numpy as np
from services.models.regional_analysis_model import build_regional_analysis_model

class RegionalAnalysisService:
    def __init__(self):
        # Модель принимает один числовой признак, полученный из региона
        self.model = build_regional_analysis_model(input_dim=1)

    def analyze(self, data, return_analysis):
        # Преобразуем регион в числовое значение (например, 'North' -> 1, остальные -> 0)
        data['Region_Encoded'] = data['Region'].apply(lambda x: 1 if x == "North" else 0)
        X = data['Region_Encoded'].values.reshape(-1, 1)
        predicted = self.model.predict(X)
        data['Priority_Score'] = predicted.flatten()
        return data
