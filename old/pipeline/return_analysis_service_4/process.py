# class ReturnAnalysisService:
#     def analyze(self, data):
#         """
#         Анализ возвратов.
#         :param data: DataFrame с характеристиками продуктов.
#         :return: DataFrame с анализом возвратов.
#         """
#         data['Return_Rate'] = data['Returns'] / data['Quantity_Sold']
#         data['High_Return_Risk'] = data['Return_Rate'].apply(lambda x: 1 if x > 0.2 else 0)
#         return data
