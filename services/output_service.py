# services/output_service.py

class OutputService:
    def generate_output(self, data, discount_impact):
        # Генерация финального вывода на основе всех данных
        output = {
            "Product_Name": "Milk",
            "Optimal_Purchase_Quantity": 500,
            "Stock_Left": 50,
            "Predicted_Demand": 450,
            "Priority_Score": 0.9,
            "Recommended_Discount": 10,
            "Expected_Returns_Rate": 5,
            "Region": "North",
            "Holiday_Impact": True
        }
        return output
