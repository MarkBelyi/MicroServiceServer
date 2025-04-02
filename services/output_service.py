# services/output_service.py

class OutputService:
    def generate_output(self, data, discount_impact):
        output_columns = [
            'Product_Name',
            'Recommended_Quantity',
            'Stock_Left',
            'Predicted_Demand',
            'Priority_Score',
            'Discount',
            'Return_Rate',
            'Region',
            'Holiday',
            'Final_Demand'
        ]
        final_df = data[output_columns].copy()
        final_df = final_df.rename(columns={
            'Recommended_Quantity': 'Optimal_Purchase_Quantity',
            'Discount': 'Recommended_Discount',
            'Return_Rate': 'Expected_Returns_Rate'
        })
        final_df.insert(0, 'id', range(1, len(final_df) + 1))
        result = final_df.to_dict(orient='records')
        return result
