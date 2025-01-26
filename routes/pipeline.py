from flask import Blueprint, request, jsonify
from pipeline.pipeline_service import PipelineService

pipeline_blueprint = Blueprint("pipeline", __name__)
pipeline_service = PipelineService()

@pipeline_blueprint.route('/execute_pipeline', methods=['POST'])
def execute_pipeline():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    try:
        recommendations = pipeline_service.execute_pipeline(file)
        return jsonify({'recommendations': recommendations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
