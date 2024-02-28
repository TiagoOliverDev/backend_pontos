from flask import Flask, request, jsonify, Blueprint
from ..repositories.auth_repository import AuthRepository
from ..services.auth_service import AuthService
from flask_bcrypt import Bcrypt

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '9ba263503b01ce2ef81f6641f504b45333aa0662183d0184db79d9e92ccef620'
# bcrypt = Bcrypt(app)
# auth_service = AuthService(app.config['SECRET_KEY'])
auth_service = AuthService('9ba263503b01ce2ef81f6641f504b45333aa0662183d0184db79d9e92ccef620')
auth_repository = AuthRepository()

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()
    username = auth_data['username']
    password = auth_data['password']

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if not auth_repository.user_exists(username):
        return jsonify({'message': 'User does not exist'}), 401

    stored_password = auth_repository.get_user_password(username)
    if not auth_service.verify_password(stored_password, password):
        return jsonify({'message': 'Invalid password'}), 401

    token = auth_service.generate_token(username)
    
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return jsonify({'token': token}), 200


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    matricula = data['matricula']
    tipo_permissao = data['tipo_permissao']

    if not all([name, email, password, matricula, tipo_permissao]):
        return jsonify({'message': 'All fields are required'}), 400

    user, error = auth_service.register_user(name, email, password, matricula, tipo_permissao)
    if error:
        return jsonify({'message': error}), 400

    return jsonify({'user': user, 'message': 'User created successfully'}), 201





