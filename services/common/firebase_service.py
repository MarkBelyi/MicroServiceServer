import firebase_admin
from firebase_admin import auth, credentials
from flask import jsonify

# Инициализация Firebase
cred = credentials.Certificate("retailshopapi-firebase-adminsdk-icty0-8c24af4a0a.json")
firebase_admin.initialize_app(cred)

class FirebaseService:
    def send_verification(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing fields'}), 400

        try:
            auth.create_user(email=email, password=password)

            # Генерируем ссылку для подтверждения email
            verification_link = auth.generate_email_verification_link(email)

            # Здесь можно отправить verification_link через сторонний сервис, например, SMTP или SendGrid
            # Для примера просто возвращаем ссылку в ответе
            return jsonify({'message': f'User created. Verification email sent to {email}',
                            'verification_link': verification_link}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
