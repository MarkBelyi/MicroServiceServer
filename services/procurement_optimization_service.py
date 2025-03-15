# services/procurement_optimization_service.py

import numpy as np
from services.models.procurement_optimization_model import build_procurement_optimization_model


class ProcurementOptimizationService:
    def __init__(self):
        # Используем два признака: Predicted_Demand и Stock_Left; выход – рекомендованное количество
        self.model = build_procurement_optimization_model(input_dim=2, output_dim=1)

    def optimize(self, data, demand_forecast, expiry_analysis):
        X = data[['Predicted_Demand', 'Stock_Left']].values
        predicted = self.model.predict(X)
        data['Recommended_Quantity'] = predicted.flatten()
        return data
