from flask import Blueprint, request, jsonify
from services.auth_services import AuthService
from flask_jwt_extended import jwt_required

auth_blueprint = Blueprint("auth", __name__)
auth_service = AuthService()

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    return auth_service.register(data)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    return auth_service.login(data)

@auth_blueprint.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    return auth_service.get_all_users()