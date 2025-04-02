from flask import Blueprint, request, jsonify
from services.pipeline_service import PipelineService

pipeline_blueprint = Blueprint('pipeline', __name__)
pipeline_service = PipelineService()

@pipeline_blueprint.route('/execute', methods=['POST'])
def execute_pipeline():
    if 'file' not in request.files:
        return jsonify({"error": "Файл не предоставлен"}), 400
    file = request.files['file']
    try:
        pipeline_service = PipelineService()
        result = pipeline_service.execute_pipeline(file)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pipeline_blueprint.route('/execute-hardcoded', methods=['GET'])
def execute_pipeline_hardcoded():
    pipeline_service = PipelineService()
    result = pipeline_service.execute_pipeline('synthetic_dataset_BETA_3.xlsx')

    return jsonify(result)
