from flask import Blueprint, jsonify

pipeline_blueprint = Blueprint('pipeline', __name__)

# Глобальная переменная-счётчик, изначально равная 0
counter = 0

def stage_0(results):
    global counter
    counter += 1
    results.append(f"Этап 0 выполнен. counter = {counter}")

def stage_1(results):
    global counter
    counter += 1
    results.append(f"Этап 1 выполнен. counter = {counter}")

def stage_2(results):
    global counter
    counter += 1
    results.append(f"Этап 2 выполнен. counter = {counter}")

def stage_3(results):
    global counter
    counter += 1
    results.append(f"Этап 3 выполнен. counter = {counter}")

def stage_4(results):
    global counter
    counter += 1
    results.append(f"Этап 4 выполнен. counter = {counter}")

def stage_5(results):
    global counter
    counter += 1
    results.append(f"Этап 5 выполнен. counter = {counter}")

def stage_6(results):
    global counter
    counter += 1
    results.append(f"Этап 6 выполнен. counter = {counter}")

def stage_7(results):
    global counter
    counter += 1
    results.append(f"Этап 7 выполнен. counter = {counter}")

def run_pipeline_logic():
    results = []
    stage_0(results)
    stage_1(results)
    stage_2(results)
    stage_3(results)
    stage_4(results)
    stage_5(results)
    stage_6(results)
    stage_7(results)
    return results


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
