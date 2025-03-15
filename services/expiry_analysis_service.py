# services/expiry_analysis_service.py

import numpy as np
import pandas as pd
from datetime import datetime
from services.models.expiry_analysis_model import build_expiry_analysis_model

class ExpiryAnalysisService:
    def __init__(self):
        # Модель принимает один признак: количество дней до окончания срока
        self.model = build_expiry_analysis_model(input_dim=1)

    def analyze(self, data, demand_forecast):
        # Используем существующий столбец "End_Expiry_Date" и сохраняем результат в новый столбец "End_Expiry"
        data['End_Expiry'] = pd.to_datetime(data['End_Expiry_Date'])
        current_date = datetime.now()
        data['Days_to_Expiry'] = (data['End_Expiry'] - current_date).dt.days
        # Подготавливаем входные данные для модели
        X = data['Days_to_Expiry'].values.reshape(-1, 1)
        predicted = self.model.predict(X)
        data['Expiration_Date_Impact'] = predicted.flatten()
        return data
