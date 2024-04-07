# service.py
from passlib.hash import bcrypt
from ..repositories.auth_repository import AuthRepository
import jwt


auth_repository = AuthRepository()

class AuthService:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def verify_password(self, stored_password, provided_password):
        return bcrypt.verify(provided_password, stored_password)

    def generate_token(self, email: str):
        payload = {'email': email}
        try:
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            return token
        except AttributeError as e:
            print(f"Erro ao tentar codificar o token: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao gerar o token: {e}")
            return None

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['email']
        except jwt.ExpiredSignatureError:
            return 'Token expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        
    def register_user(self, name: str, email: str, password: str, matricula: str, tipo_permissao: int):
        if auth_repository.get_user_by_email(email):
            return None, 'Email already exists'

        user = auth_repository.create_user(name, email, password, matricula, tipo_permissao)
        return user, None
