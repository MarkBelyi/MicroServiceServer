

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

    def execute_pipeline(self, input_file):
        # 0. Загрузка данных
        data = self.upload_service.upload(input_file)

        # 1. Прогноз спроса
        demand_forecast = self.forecasting_service.forecast(data)

        # 2. Анализ срока годности
        expiry_analysis = self.expiry_analysis_service.analyze(data, demand_forecast)

        # 3. Оптимизация закупок
        optimized_procurement = self.procurement_optimization_service.optimize(data, demand_forecast, expiry_analysis)

        # 4. Анализ возвратов
        return_analysis = self.return_analysis_service.analyze(data, optimized_procurement)

        # 5. Региональные особенности
        regional_analysis = self.regional_analysis_service.analyze(data, return_analysis)

        # 6. Влияние скидок и праздников
        discount_impact = self.discount_impact_service.analyze(data, regional_analysis)

        # 7. Генерация рекомендаций
        final_output = self.output_service.generate_output(data, discount_impact)

        return final_output
