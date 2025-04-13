# services/output_service.py
import pandas as pd


# class OutputService:
#     def generate_output(self, data, discount_impact):
#         output_columns = [
#             'Product_Name',
#             'Recommended_Quantity',
#             'Stock_Left',
#             'Predicted_Demand',
#             'Priority_Score',
#             'Discount',
#             'Return_Rate',
#             'Region',
#             'Holiday',
#             'Final_Demand'
#         ]
#         final_df = data[output_columns].copy()
#         final_df = final_df.rename(columns={
#             'Recommended_Quantity': 'Optimal_Purchase_Quantity',
#             'Discount': 'Recommended_Discount',
#             'Return_Rate': 'Expected_Returns_Rate'
#         })
#         final_df.insert(0, 'id', range(1, len(final_df) + 1))
#         result = final_df.to_dict(orient='records')
#         return result

class OutputService:
    def generate_output(self, data: pd.DataFrame):
        # Ожидаемые столбцы для финального результата
        expected_columns = [
            'Product_Name',
            'Прогнозируемые продажи',
            'Текущий запас',
            'Запас безопасности',
            'Рекомендуемое количество к закупке'
        ]
        available_columns = [col for col in expected_columns if col in data.columns]
        if len(available_columns) < len(expected_columns):
            missing = set(expected_columns) - set(available_columns)
            raise KeyError(f"Отсутствуют обязательные столбцы: {missing}")

        # Формируем итоговый DataFrame и добавляем уникальный идентификатор
        final_df = data[available_columns].copy()
        final_df.insert(0, 'id', range(1, len(final_df) + 1))
        result = final_df.to_dict(orient='records')
        return result

