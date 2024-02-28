from flask import Flask, request, jsonify, Blueprint
from repositories import AuthRepository
from services import AuthService
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ba263503b01ce2ef81f6641f504b45333aa0662183d0184db79d9e92ccef620'
bcrypt = Bcrypt(app)
auth_service = AuthService(app.config['SECRET_KEY'])
auth_repository = AuthRepository()

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()
    username = auth_data.get('username')
    password = auth_data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if not auth_repository.user_exists(username):
        return jsonify({'message': 'User does not exist'}), 401

    stored_password = auth_repository.get_user_password(username)
    if not auth_service.verify_password(stored_password, password):
        return jsonify({'message': 'Invalid password'}), 401

    token = auth_service.generate_token(username)
    return jsonify({'token': token.decode('utf-8')}), 200


