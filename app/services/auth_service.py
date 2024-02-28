# service.py
from passlib.hash import bcrypt
import jwt

class AuthService:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def verify_password(self, stored_password, provided_password):
        return bcrypt.verify(provided_password, stored_password)

    def generate_token(self, username):
        payload = {'username': username}
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['username']
        except jwt.ExpiredSignatureError:
            return 'Token expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
