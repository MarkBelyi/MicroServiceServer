# services/demand_forecasting_service.py

import numpy as np
from services.models.demand_forecasting_model import build_demand_forecasting_model

class DemandForecastingService:
    def __init__(self):
        self.model = build_demand_forecasting_model(input_shape=(1, 1))

    def forecast(self, data):
        grouped = data.groupby(
            'Product_Name',
            as_index=False
        ).agg({
            'Company': 'first',
            'Quantity_Sold': 'sum',
            'Stock_Left': 'sum',
            'Returns': 'sum',
            'Discount': 'mean',
            'Start_Expiry_Date': 'min',
            'End_Expiry_Date': 'min',
            'Purchase_Date': 'min',
            'Sales_Date': 'max',
            'Purchase_Price': 'mean',
            'Selling_Price': 'mean',
            'Holiday': 'mean',
            'Subgroup': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
            'Season': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
            'Region': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0]
        })

        X = grouped['Quantity_Sold'].values.reshape(-1, 1, 1)
        predicted = self.model.predict(X)
        grouped['Predicted_Demand'] = predicted.flatten()
        return grouped
