import pandas as pd
import numpy as np
import datetime
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, LSTM, Dropout, BatchNormalization, Input, Flatten
from tensorflow.keras.optimizers import Adam


# =====================================
# Функции построения нейронных сетей
# =====================================

# 1. Модель прогнозирования спроса (LSTM)
def build_demand_forecasting_model(sequence_length, forecast_horizon):
    model = Sequential()
    model.add(LSTM(64, activation='tanh', return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(LSTM(32, activation='tanh'))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(Dense(forecast_horizon, activation='linear'))
    model.compile(optimizer=Adam(), loss='mse')
    return model


# 2. Модель анализа срока годности (FCNN)
def build_expiry_model():
    model = Sequential()
    model.add(Dense(16, activation='relu', input_shape=(2,)))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=Adam(), loss='binary_crossentropy')
    return model


# 3. Модель оптимизации закупок (FCNN)
def build_procurement_model():
    model = Sequential()
    model.add(Dense(16, activation='relu', input_shape=(2,)))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer=Adam(), loss='mse')
    return model


# 4. Модель анализа возвратов (FCNN)
def build_return_model():
    model = Sequential()
    model.add(Dense(8, activation='relu', input_shape=(1,)))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer=Adam(), loss='mse')
    return model


# 5. Модель регионального анализа (FCNN)
def build_regional_model():
    model = Sequential()
    model.add(Dense(8, activation='relu', input_shape=(1,)))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer=Adam(), loss='mse')
    return model


# 6. Модель влияния скидок и праздников (FCNN)
def build_discount_model():
    model = Sequential()
    model.add(Dense(16, activation='relu', input_shape=(2,)))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(2, activation='sigmoid'))
    model.compile(optimizer=Adam(), loss='mse')
    return model


# =====================================
# Сервисы (модули) пайплайна с NN
# =====================================

# Сервис загрузки данных из Excel
class UploadService:
    def upload(self, file_path: str) -> pd.DataFrame:
        print("Запуск UploadService: загрузка данных")
        df = pd.read_excel(file_path)
        # Приведение к типу datetime для полей с датой, если они присутствуют
        if 'Sales_Date' in df.columns:
            df['Sales_Date'] = pd.to_datetime(df['Sales_Date'])
        if 'End_Expiry' in df.columns:
            df['End_Expiry'] = pd.to_datetime(df['End_Expiry'])
        print("Данные успешно загружены. Количество записей:", df.shape[0])
        return df


# Сервис прогнозирования спроса на основе временных рядов (LSTM)
class DemandForecastingService:
    def __init__(self):
        self.sequence_length = 90
        self.forecast_horizon = 30
        self.model = build_demand_forecasting_model(self.sequence_length, self.forecast_horizon)
        self.expected_columns = [
            'Product_Name',
            'Прогнозируемые продажи',
            'Текущий запас',
            'Запас безопасности',
            'Рекомендуемое количество к закупке'
        ]

    def forecast(self, data: pd.DataFrame) -> pd.DataFrame:
        print("Запуск DemandForecastingService: прогнозирование спроса")
        # Группируем данные по продукту и дате
        sales = data.groupby(['Product_Name', 'Sales_Date']).agg({
            'Quantity_Sold': 'sum',
            'Stock_Left': 'max'
        }).reset_index()
        results = []
        for product in data['Product_Name'].unique():
            prod_sales = sales[sales['Product_Name'] == product].set_index('Sales_Date').asfreq('D').fillna(0)
            # Получаем все записи продаж продукта
            train_series = prod_sales['Quantity_Sold'].values.astype(np.float32)
            # Если данных меньше, чем требуется, дополняем слева нулями до длины self.sequence_length
            if len(train_series) < self.sequence_length:
                pad_length = self.sequence_length - len(train_series)
                train_series = np.pad(train_series, (pad_length, 0), 'constant')
            else:
                train_series = train_series[-self.sequence_length:]
            X = train_series.reshape(1, self.sequence_length, 1)
            # Демонстрационный target: повтор среднего значения за train_series
            y_target = np.full((1, self.forecast_horizon), train_series.mean(), dtype=np.float32)
            # Обучаем модель на данном малом наборе
            self.model.fit(X, y_target, epochs=5, verbose=0)
            pred = self.model.predict(X)
            predicted_sales = pred.sum()
            current_stock = prod_sales['Stock_Left'].iloc[-1]
            safety_stock = 0.15 * predicted_sales
            rec_qty = max(predicted_sales - current_stock + safety_stock, 0)
            results.append({
                'Product_Name': product,
                'Прогнозируемые продажи': round(predicted_sales),
                'Текущий запас': current_stock,
                'Запас безопасности': round(safety_stock),
                'Рекомендуемое количество к закупке': round(rec_qty)
            })
        if not results:
            forecast_df = pd.DataFrame(columns=self.expected_columns)
        else:
            forecast_df = pd.DataFrame(results, columns=self.expected_columns)
        print("DemandForecastingService завершён. Прогноз получен для", forecast_df.shape[0], "продуктов.")
        return forecast_df


# Сервис анализа срока годности (FCNN)
class ExpiryAnalysisService:
    def __init__(self):
        self.model = build_expiry_model()

    def analyze(self, forecast_df: pd.DataFrame, original_data: pd.DataFrame) -> pd.DataFrame:
        print("Запуск ExpiryAnalysisService: анализ срока годности")
        # Если forecast_df пуст, возвращаем его с нужным столбцом
        if forecast_df.empty:
            forecast_df['Expiration_Date_Impact'] = []
            print("ExpiryAnalysisService: Нет данных для анализа срока годности.")
            return forecast_df

        impact_scores = []
        for product in forecast_df['Product_Name']:
            subset = original_data[original_data['Product_Name'] == product]
            if 'End_Expiry' in subset.columns and not subset.empty:
                last_sale = subset['Sales_Date'].max()
                days_diff = (subset['End_Expiry'] - last_sale).dt.days.min()
                norm_days = np.clip(days_diff, 0, 100) / 100.0
            else:
                norm_days = 1.0
            current_stock = subset['Stock_Left'].max() if 'Stock_Left' in subset.columns else 0
            norm_stock = current_stock / 1000.0
            features = np.array([[norm_days, norm_stock]])
            risk = self.model.predict(features)[0][0]
            impact_scores.append(risk)
        df = forecast_df.copy()
        df['Expiration_Date_Impact'] = impact_scores
        print("ExpiryAnalysisService завершён.")
        return df


# Сервис оптимизации закупок (FCNN)
class ProcurementOptimizationService:
    def __init__(self):
        self.model = build_procurement_model()

    def optimize(self, data: pd.DataFrame, original_data: pd.DataFrame) -> pd.DataFrame:
        print("Запуск ProcurementOptimizationService: оптимизация закупок")
        optimized_qty = []
        for idx, row in data.iterrows():
            input_feat = np.array([[row['Рекомендуемое количество к закупке'], row['Expiration_Date_Impact']]])
            target = np.array([[row['Рекомендуемое количество к закупке']]])
            self.model.fit(input_feat, target, epochs=3, verbose=0)
            opt_val = self.model.predict(input_feat)[0][0]
            optimized_qty.append(round(opt_val))
        df = data.copy()
        df['Optimal_Purchase_Quantity'] = optimized_qty
        print("ProcurementOptimizationService завершён.")
        return df


# Сервис анализа возвратов (FCNN)
class ReturnAnalysisService:
    def __init__(self):
        self.model = build_return_model()

    def analyze(self, data: pd.DataFrame, original_data: pd.DataFrame) -> pd.DataFrame:
        print("Запуск ReturnAnalysisService: анализ возвратов")
        expected_returns = []
        for product in data['Product_Name']:
            subset = original_data[original_data['Product_Name'] == product]
            if 'Returns' in subset.columns and subset['Quantity_Sold'].sum() > 0:
                hist_rate = (subset['Returns'].sum() / subset['Quantity_Sold'].sum()) * 100.0
            else:
                hist_rate = 5.0
            X = np.array([[hist_rate]])
            self.model.fit(X, X, epochs=3, verbose=0)
            predicted_rate = self.model.predict(X)[0][0]
            expected_returns.append(round(predicted_rate, 2))
        df = data.copy()
        df['Expected_Returns_Rate'] = expected_returns
        print("ReturnAnalysisService завершён.")
        return df


# Сервис регионального анализа (FCNN)
class RegionalAnalysisService:
    def __init__(self):
        self.model = build_regional_model()

    def analyze(self, data: pd.DataFrame, original_data: pd.DataFrame) -> pd.DataFrame:
        print("Запуск RegionalAnalysisService: анализ региональных особенностей")
        regions = []
        regional_demands = []
        for product in data['Product_Name']:
            subset = original_data[original_data['Product_Name'] == product]
            if 'Region' in subset.columns and not subset['Region'].empty:
                mode_reg = subset['Region'].mode().iloc[0]
            else:
                mode_reg = "Unknown"
            regions.append(mode_reg)
            total_sales = subset['Quantity_Sold'].sum() if 'Quantity_Sold' in subset.columns else 0
            X = np.array([[total_sales]])
            self.model.fit(X, X, epochs=3, verbose=0)
            regional_score = self.model.predict(X)[0][0]
            regional_demands.append(round(regional_score))
        df = data.copy()
        df['Region'] = regions
        df['Regional_Demand'] = regional_demands
        print("RegionalAnalysisService завершён.")
        return df


# Сервис анализа влияния скидок и праздников (FCNN)
class DiscountImpactService:
    def __init__(self):
        self.model = build_discount_model()

    def analyze(self, data: pd.DataFrame, original_data: pd.DataFrame) -> pd.DataFrame:
        print("Запуск DiscountImpactService: анализ влияния скидок и праздников")
        discount_impacts = []
        holiday_impacts = []
        for product in data['Product_Name']:
            subset = original_data[original_data['Product_Name'] == product]
            if 'Discount' in subset.columns:
                avg_discount = subset['Discount'].mean()
            else:
                avg_discount = 0.0
            if 'Holiday' in subset.columns:
                holiday_vals = subset['Holiday'].apply(lambda x: 1 if str(x).lower() in ['yes', 'true', '1'] else 0)
                avg_holiday = 1.0 if holiday_vals.mean() > 0.5 else 0.0
            else:
                avg_holiday = 0.0
            input_feat = np.array([[avg_discount / 100.0, avg_holiday]])
            self.model.fit(input_feat, input_feat, epochs=3, verbose=0)
            pred = self.model.predict(input_feat)[0]
            discount_impacts.append(round(pred[0], 2))
            holiday_impacts.append(1 if pred[1] > 0.5 else 0)
        df = data.copy()
        df['Discount_Impact'] = discount_impacts
        df['Holiday_Impact'] = holiday_impacts
        print("DiscountImpactService завершён.")
        return df


# Сервис формирования финального вывода
class OutputService:
    def generate_output(self, data: pd.DataFrame):
        print("Запуск OutputService: формирование финального вывода")
        expected_columns = [
            'Product_Name',
            'Optimal_Purchase_Quantity',
            'Текущий запас',
            'Прогнозируемые продажи',
            'Expected_Returns_Rate',
            'Region',
            'Discount_Impact',
            'Holiday_Impact',
            'Regional_Demand',
            'Expiration_Date_Impact'
        ]
        missing = set(expected_columns) - set(data.columns)
        if missing:
            raise KeyError(f"Отсутствуют обязательные столбцы: {missing}")
        final_df = data[expected_columns].copy()
        final_df.insert(0, 'id', range(1, len(final_df) + 1))
        print("OutputService завершён. Формирование финального вывода закончено.")
        return final_df.to_dict(orient='records')


# =====================================
# Основной пайплайн
# =====================================
class PipelineService:
    def __init__(self):
        self.upload_service = UploadService()
        self.forecasting_service = DemandForecastingService()
        self.expiry_analysis_service = ExpiryAnalysisService()
        self.procurement_optimization_service = ProcurementOptimizationService()
        self.return_analysis_service = ReturnAnalysisService()
        self.regional_analysis_service = RegionalAnalysisService()
        self.discount_impact_service = DiscountImpactService()
        self.output_service = OutputService()

    def execute_pipeline(self, input_file: str):
        print("Начало выполнения пайплайна.")
        original_data = self.upload_service.upload(input_file)
        print("Исходные данные загружены.")

        print("Запуск этапа прогнозирования спроса...")
        forecast_df = self.forecasting_service.forecast(original_data)
        print("Этап прогнозирования завершён.")

        print("Запуск этапа анализа срока годности...")
        expiry_df = self.expiry_analysis_service.analyze(forecast_df, original_data)
        print("Этап анализа срока годности завершён.")

        print("Запуск этапа оптимизации закупок...")
        proc_df = self.procurement_optimization_service.optimize(expiry_df, original_data)
        print("Этап оптимизации закупок завершён.")

        print("Запуск этапа анализа возвратов...")
        return_df = self.return_analysis_service.analyze(proc_df, original_data)
        print("Этап анализа возвратов завершён.")

        print("Запуск этапа регионального анализа...")
        regional_df = self.regional_analysis_service.analyze(return_df, original_data)
        print("Этап регионального анализа завершён.")

        print("Запуск этапа анализа влияния скидок и праздников...")
        discount_df = self.discount_impact_service.analyze(regional_df, original_data)
        print("Этап анализа влияния скидок и праздников завершён.")

        print("Формирование финального вывода...")
        final_output = self.output_service.generate_output(discount_df)
        print("Пайплайн успешно завершён.")
        return final_output


# =====================================
# Запуск пайплайна
# =====================================
if __name__ == "__main__":
    input_file_path = "synthetic_dataset_BETA_3.xlsx"
    pipeline = PipelineService()
    output = pipeline.execute_pipeline(input_file_path)
    print("Итоговый вывод:")
    print(output)
