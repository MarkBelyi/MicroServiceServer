class ExpiryAnalysisService:
    def analyze(self, data):
        """
        Анализ срока годности продуктов.
        :param data: DataFrame с характеристиками продуктов.
        :return: DataFrame с анализом срока годности.
        """
        data['Days_To_Expiry'] = (data['End_Expiry_Date'] - data['Sales_Date']).dt.days
        data['Expiry_Risk'] = data['Days_To_Expiry'].apply(lambda x: 1 if x <= 0 else 0)
        return data
