import pickle

class ProcurementOptimizationService:
    def __init__(self):
        self.model_path = 'pipeline/3_procurement_optimization_service/knapsack_model_2.pkl'

    def load_model(self):
        with open(self.model_path, 'rb') as f:
            return pickle.load(f)

    def optimize(self, data):
        """
        Оптимизация закупок.
        :param data: DataFrame с характеристиками продуктов.
        :return: DataFrame с оптимизированными закупками.
        """
        model = self.load_model()
        weights = data['Purchase_Price']
        values = data['Predicted_Demand']
        capacity = 10000  # Максимальный бюджет
        optimized_indices = model.optimize(weights, values, capacity)
        data['Optimized_Procurement'] = 0
        data.loc[optimized_indices, 'Optimized_Procurement'] = 1
        return data
