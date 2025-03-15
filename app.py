from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from instance.models.user import db
from routes.auth import auth_blueprint
from routes.firebase import firebase_blueprint
from routes.pipeline import pipeline_blueprint

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(firebase_blueprint, url_prefix="/firebase")
app.register_blueprint(pipeline_blueprint, url_prefix="/pipeline")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)