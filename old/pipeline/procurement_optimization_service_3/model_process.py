from scipy.optimize import linprog

class ProcurementOptimizationService:
    def optimize(self, data):
        c = -data['Predicted_Demand'].values  # Максимизация прибыли (отрицательная стоимость)
        A_eq = [data['Purchase_Price'].values]
        b_eq = [data['Budget'].sum()]
        bounds = [(0, stock) for stock in data['Stock_Left']]

        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
        return {'optimized_allocation': result.x, 'status': result.message}
