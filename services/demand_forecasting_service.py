# services/demand_forecasting_service.py
from keras.src.callbacks import EarlyStopping
from services.models.demand_forecasting_model import build_demand_forecasting_model
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# class DemandForecastingService:
#     def __init__(self):
#         self.model = build_demand_forecasting_model(input_shape=(1, 1))
#
#     def forecast(self, data):
#         grouped = data.groupby(
#             'Product_Name',
#             as_index=False
#         ).agg({
#             'Company': 'first',
#             'Quantity_Sold': 'sum',
#             'Stock_Left': 'sum',
#             'Returns': 'sum',
#             'Discount': 'mean',
#             'Start_Expiry_Date': 'min',
#             'End_Expiry_Date': 'min',
#             'Purchase_Date': 'min',
#             'Sales_Date': 'max',
#             'Purchase_Price': 'mean',
#             'Selling_Price': 'mean',
#             'Holiday': 'mean',
#             'Subgroup': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
#             'Season': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
#             'Region': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0]
#         })
#
#         X = grouped['Quantity_Sold'].values.reshape(-1, 1, 1)
#         predicted = self.model.predict(X)
#         grouped['Predicted_Demand'] = predicted.flatten()
#         return grouped


class DemandForecastingService:
    def __init__(self):
        # Используем 4 входных параметра: Quantity_Sold, Stock_Left, Discount и Returns
        self.num_features = 4
        self.model = build_demand_forecasting_model(input_shape=(1, self.num_features))
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()

    def forecast(self, data: pd.DataFrame) -> pd.DataFrame:
        # Группировка данных по продукту с агрегацией нескольких параметров
        grouped = data.groupby('Product_Name', as_index=False).agg({
            'Quantity_Sold': 'sum',
            'Stock_Left': 'sum',
            'Discount': 'mean',
            'Returns': 'sum'
        })

        # Расчёт оптимального количества закупок: если остаток меньше продаж, то нужно докупить разницу
        grouped['Optimal_Purchase_Quantity'] = grouped.apply(
            lambda row: max(row['Quantity_Sold'] - row['Stock_Left'], 0), axis=1
        )

        # Выбираем входные признаки
        features = ['Quantity_Sold', 'Stock_Left', 'Discount', 'Returns']
        X = grouped[features].values.astype(np.float32)
        y = grouped[['Optimal_Purchase_Quantity']].values.astype(np.float32)

        # Нормализация входных данных и целевого значения
        X_norm = self.scaler_X.fit_transform(X)
        y_norm = self.scaler_y.fit_transform(y)

        # Преобразование X для LSTM: (samples, timesteps, features)
        X_norm = X_norm.reshape(-1, 1, self.num_features)

        # Обучение модели "на лету" с использованием ранней остановки
        early_stopping = EarlyStopping(monitor='loss', patience=100, restore_best_weights=True, verbose=1)
        self.model.fit(X_norm, y_norm, epochs=50, callbacks=[early_stopping], verbose=0)

        # Прогнозирование оптимального количества закупок (нормализованное значение)
        predicted_norm = self.model.predict(X_norm)
        # Выбираем только первый столбец, чтобы получить форму (samples, 1)
        predicted = self.scaler_y.inverse_transform(predicted_norm[:, 0].reshape(-1, 1))
        # Приводим отрицательные значения к 0
        predicted = np.clip(predicted, 0, None)
        grouped['Predicted_Purchase_Quantity'] = predicted.flatten()

        return grouped