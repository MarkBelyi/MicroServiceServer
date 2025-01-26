from flask import jsonify
from models.user import db, User
from flask_jwt_extended import create_access_token
from utils.hash import hash_password, verify_password

class AuthService:
    def register(self, data):
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return jsonify({'error': 'Missing fields'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        hashed_password = hash_password(password)
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    def login(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Missing fields'}), 400

        user = User.query.filter_by(username=username).first()
        if not user or not verify_password(password, user.password):
            return jsonify({'error': 'Invalid username or password'}), 401

        access_token = create_access_token(identity={'username': username})
        return jsonify({'token': access_token}), 200

    def get_all_users(self):
        users = User.query.all()
        users_list = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            for user in users
        ]
        return jsonify({'users': users_list}), 200
