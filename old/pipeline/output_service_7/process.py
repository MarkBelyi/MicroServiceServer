# class OutputService:
#     def generate_output(self, data):
#         """
#         Генерация рекомендаций.
#         :param data: DataFrame с анализом продуктов.
#         :return: Рекомендации.
#         """
#         best_products = data.sort_values(by='Discount_Impact', ascending=False).head(10)
#         return best_products.to_dict(orient='records')
