
from services.upload_service import UploadService
from services.demand_forecasting_service import DemandForecastingService
from services.expiry_analysis_service import ExpiryAnalysisService
from services.procurement_optimization_service import ProcurementOptimizationService
from services.return_analysis_service import ReturnAnalysisService
from services.regional_analysis_service import RegionalAnalysisService
from services.discount_impact_service import DiscountImpactService
from services.output_service import OutputService


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
        data = self.forecasting_service.forecast(data)

        # # 2. Анализ срока годности
        # data = self.expiry_analysis_service.analyze(data, data)
        #
        # # 3. Оптимизация закупок
        # data = self.procurement_optimization_service.optimize(data, data, data)
        #
        # # 4. Анализ возвратов
        # data = self.return_analysis_service.analyze(data, data)
        #
        # # 5. Региональные особенности
        # data = self.regional_analysis_service.analyze(data, data)
        #
        # # 6. Влияние скидок и праздников
        # data = self.discount_impact_service.analyze(data, data)
        #
        # # 7. Генерация рекомендаций
        final_output = self.output_service.generate_output(data)

        return final_output
