from flask import Flask, request, jsonify, Blueprint
from ..repositories.auth_repository import AuthRepository
from ..services.auth_service import AuthService
from flask_bcrypt import Bcrypt
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
auth_service = AuthService(SECRET_KEY)
auth_repository = AuthRepository()

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()

    email = auth_data['email']
    password = auth_data['password']
    id_user = auth_repository.get_id_user(email=email)
    type_permission = auth_repository.get_type_permission_user(email=email)

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    if not auth_repository.email_user_exists(email):
        return jsonify({'message': 'User does not exist'}), 401

    stored_password = auth_repository.get_user_password(email)
    if not auth_service.verify_password(stored_password, password):
        return jsonify({'message': 'Invalid password'}), 401

    token = auth_service.generate_token(email)
    
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return jsonify({'id_user': id_user, 'BearerToken': token, 'type_permission': type_permission}), 200


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    name = data['name']
    email = data['email']
    password = data['senha']
    matricula = data['matricula']
    tipo_permissao = 2 # 2 = usuário admin
    # tipo_permissao = data['tipo_permissao']

    if not all([name, email, password, matricula, tipo_permissao]):
        return jsonify({'message': 'All fields are required'}), 400

    user, error = auth_service.register_user(name, email, password, matricula, tipo_permissao)
    if error:
        return jsonify({'message': error}), 400

    return jsonify({'user': user, 'message': 'User created successfully'}), 201





