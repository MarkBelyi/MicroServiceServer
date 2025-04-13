import numpy as np
from keras import Sequential
from keras.src.callbacks import EarlyStopping
from keras.src.layers import LSTM, Dropout, Dense
import pandas as pd

# Сервис прогнозирования закупок с использованием нейронной сети (LSTM)
class DemandForecastingService:
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Преобразует поле Sales_Date в тип datetime и группирует данные по Product_Name и Sales_Date:
          - Quantity_Sold: суммируются продажи за день
          - Stock_Left: берется максимальное значение остатка за день
        """
        data['Sales_Date'] = pd.to_datetime(data['Sales_Date'])
        grouped = data.groupby(['Product_Name', 'Sales_Date']).agg({
            'Quantity_Sold': 'sum',
            'Stock_Left': 'max'
        }).reset_index()
        return grouped

    def create_lag_data(self, series: pd.Series, n_lags: int):
        """
        Создает обучающий набор для нейронной сети:
          X - массив лаговых признаков (последовательности длины n_lags),
          y - целевое значение (следующий день после последовательности).
        """
        X, y = [], []
        values = series.values
        for i in range(n_lags, len(values)):
            X.append(values[i - n_lags:i])
            y.append(values[i])
        X = np.array(X)
        y = np.array(y)
        # Добавляем измерение признака (feature dimension), т.к. данные одномерные.
        X = X.reshape((X.shape[0], X.shape[1], 1))
        return X, y

    def build_nn_model(self, input_shape):
        """
        Строит модель LSTM:
          - Два LSTM-слоя с Dropout для регуляризации,
          - Выходной Dense-слой с одним нейроном для регрессии (предсказания продаж).
        """
        model = Sequential()
        model.add(LSTM(64, activation='tanh', return_sequences=True, input_shape=input_shape))
        model.add(Dropout(0.2))
        model.add(LSTM(32, activation='tanh'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        return model

    def forecast_product_nn(self, train: pd.Series, forecast_horizon: int = 30, n_lags: int = 7) -> float:
        """
        Прогнозирует суммарные продажи на forecast_horizon дней для одного продукта с использованием LSTM.
        Если данных меньше, чем n_lags+1, используется среднее значение за день * forecast_horizon.
        Алгоритм:
         1. Создаем обучающую выборку с лаговыми признаками из ряда train.
         2. Обучаем модель LSTM.
         3. Используем итеративное прогнозирование: для каждого следующего дня создаём окно,
            которое обновляется с учетом предсказанных значений.
         4. Возвращается сумма прогнозных значений за forecast_horizon дней.
        """
        if len(train) < n_lags + 1:
            return train.mean() * forecast_horizon

        # Формируем обучающий набор
        X_train, y_train = self.create_lag_data(train, n_lags)
        input_shape = (X_train.shape[1], X_train.shape[2])
        model = self.build_nn_model(input_shape)

        # Обучаем модель с ранней остановкой
        early_stop = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
        model.fit(X_train, y_train, epochs=100, verbose=0, callbacks=[early_stop])

        # Итеративное прогнозирование на forecast_horizon дней
        forecast_values = []
        # Инициализируем окно последними n_lags значениями из train
        last_window = list(train.values[-n_lags:])
        for _ in range(forecast_horizon):
            X_input = np.array(last_window).reshape(1, n_lags, 1)
            pred = model.predict(X_input, verbose=0)[0][0]
            forecast_values.append(pred)
            # Обновляем окно: удаляем первый элемент и добавляем предсказанное значение
            last_window.pop(0)
            last_window.append(pred)

        predicted_sales = np.sum(forecast_values)
        return predicted_sales

    def compute_order_quantity(self, predicted_sales: float, current_stock: float) -> (float, float):
        """
        Вычисляет запас безопасности (15% от прогнозируемых продаж) и рекомендуемое количество закупки:
          order_quantity = predicted_sales - current_stock + safety_stock,
        результат не может быть отрицательным.
        """
        safety_stock = 0.15 * predicted_sales
        order_quantity = max(predicted_sales - current_stock + safety_stock, 0)
        return safety_stock, order_quantity

    def forecast(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Основной метод сервиса:
         1. Преобразует и группирует исходные данные.
         2. Для каждого продукта:
             - Используются последние 90 дней данных (если доступно, иначе весь ряд) для обучения модели.
             - С помощью LSTM прогнозируются суммарные продажи на forecast_horizon (30 дней).
             - Рассчитываются текущий запас, запас безопасности и рекомендуемое количество закупки.
         3. Формируется итоговая таблица с результатами.
        """
        sales = self.preprocess_data(data)
        results = []

        for product in data['Product_Name'].unique():
            # Фильтруем данные для продукта, задаем ежедневную частоту и заполняем пропуски нулями
            prod_data = sales[sales['Product_Name'] == product] \
                .set_index('Sales_Date') \
                .asfreq('D') \
                .fillna(0)

            # Выбираем последние 90 дней продаж (если данных меньше – используются все)
            train_series = prod_data[-90:]['Quantity_Sold']
            predicted_sales = self.forecast_product_nn(train_series, forecast_horizon=30, n_lags=7)
            current_stock = prod_data['Stock_Left'].iloc[-1]
            safety_stock, order_quantity = self.compute_order_quantity(predicted_sales, current_stock)

            results.append({
                'Product_Name': product,
                'Прогнозируемые продажи': round(predicted_sales),
                'Текущий запас': current_stock,
                'Запас безопасности': round(safety_stock),
                'Рекомендуемое количество к закупке': round(order_quantity)
            })

        results_df = pd.DataFrame(results)
        return results_df
