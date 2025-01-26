from flask import Blueprint, request
from services.firebase_service import FirebaseService

firebase_blueprint = Blueprint("firebase", __name__)
firebase_service = FirebaseService()

@firebase_blueprint.route('/send-verification', methods=['POST'])
def send_verification():
    data = request.json
    return firebase_service.send_verification(data)
