import pandas as pd
from flask import jsonify


class UploadService:
    def __init__(self):
        self.required_columns = ["Product_Name", "Demand_History", "Stock_Left", "Days_To_Expire", "Region", "Returns"]

    def upload(self, file_path):
        """
        Загружает файл и проверяет его содержимое.

        :param file_path: Путь к файлу (например, .xlsx или .csv)
        :return: DataFrame с загруженными данными
        """
        try:
            # Загрузка данных из Excel
            data = pd.read_excel(file_path)

            # Проверка на наличие необходимых столбцов
            missing_columns = [col for col in self.required_columns if col not in data.columns]
            if missing_columns:
                return jsonify({"error": f"Missing columns: {missing_columns}"}), 400

            # Очистка данных (можно добавить больше шагов)
            data = self.preprocess(data)
            return data
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def preprocess(self, data):
        """
        Обрабатывает данные: заполняет пропуски, преобразует типы и т.д.

        :param data: DataFrame с сырыми данными
        :return: Обработанный DataFrame
        """
        # Заполнение пропусков
        data.fillna({"Stock_Left": 0, "Days_To_Expire": 0, "Returns": 0}, inplace=True)

        # Преобразование строкового столбца в массив (если требуется для временных рядов)
        if "Demand_History" in data.columns:
            data["Demand_History"] = data["Demand_History"].apply(
                lambda x: eval(x) if isinstance(x, str) else x
            )

        return data
