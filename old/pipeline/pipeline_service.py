from old.pipeline.upload_service_0.process import UploadService
from old.pipeline.demand_forecasting_service_1.process import DemandForecastingService
from old.pipeline.expiry_analysis_service_2.process import ExpiryAnalysisService
from old.pipeline.procurement_optimization_service_3.process import ProcurementOptimizationService
from old.pipeline.return_analysis_service_4.process import ReturnAnalysisService
from old.pipeline.regional_analysis_service_5.process import RegionalAnalysisService
from old.pipeline.discount_impact_service_6.process import DiscountImpactService
from old.pipeline.output_service_7.process import OutputService

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

        # discount_impact_service_6. Влияние скидок и праздников
        discount_impact = self.discount_impact_service.analyze(data, regional_analysis)

        # output_service_7. Генерация рекомендаций
        recommendations = self.output_service.generate_output(data, discount_impact)

        return recommendations