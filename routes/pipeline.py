from flask import Blueprint, request, jsonify
from old.pipeline.pipeline_service import PipelineService
from services.pipeline_service import run_pipeline_logic, counter

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


@pipeline_blueprint.route('/check', methods=['GET'])
def pipeline_endpoint():
    results = run_pipeline_logic()
    return jsonify({
        "pipeline_steps": results,
        "final_counter": counter
    })

