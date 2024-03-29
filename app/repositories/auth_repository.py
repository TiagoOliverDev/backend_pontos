from passlib.hash import bcrypt
from .db import Db
import logging
import psycopg2

db = Db()

class AuthRepository():
    def __init__(self):
        pass

    def user_exists(self, username: str):
        try:
            with db.connect("user_exists") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT nome FROM usuario WHERE nome = %s"
                    cursor.execute(query, (username,))
                    user = cursor.fetchone()
                    return user[0] if user else None
        except psycopg2.Error as e:
            logging.error(f"Erro ao verificar se o usuário existe: {e}")
            return None
        
    def email_user_exists(self, email: str):
        try:
            with db.connect("user_exists") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT email FROM usuario WHERE email = %s"
                    cursor.execute(query, (email,))
                    user = cursor.fetchone()
                    return user[0] if user else None
        except psycopg2.Error as e:
            logging.error(f"Erro ao verificar se o usuário existe: {e}")
            return None
               
    def get_id_user(self, email: str):
        try:
            with db.connect("get_id_user") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT id_usuario FROM usuario WHERE email = %s"
                    cursor.execute(query, (email,))
                    user = cursor.fetchone()
                    return user[0] if user else None
        except psycopg2.Error as e:
            logging.error(f"Erro ao verificar se o usuário existe: {e}")
            return None
    
    def get_type_permission_user(self, email: str):
        try:
            with db.connect("get_type_permission_user") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT u.tipo_permissao FROM usuario u WHERE email = %s"
                    cursor.execute(query, (email,))
                    permission = cursor.fetchone()
                    return permission[0] if permission else None
        except psycopg2.Error as e:
            logging.error(f"Erro ao verificar se o usuário existe: {e}")
            return None
        
    def get_user_password(self, email: str):
        try:
            with db.connect("get_user_password") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT senha FROM usuario WHERE email = %s"
                    cursor.execute(query, (email,))
                    user = cursor.fetchone()
                    return user[0] if user else None
        except psycopg2.Error as e:
            logging.error(f"Erro ao obter senha do usuário: {e}")
            return None

    def get_user_by_email(self, email: str):
        try:
            with db.connect("get_user_by_email") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT * FROM usuario WHERE email = %s"
                    cursor.execute(query, (email,))
                    user = cursor.fetchone()
                    if user:
                        return {
                            # 'id': user[0],
                            'email': user[3],
                            # 'nome': user[1],
                        }
        except psycopg2.Error as e:
            logging.error(f"Erro ao obter usuário por e-mail: {e}")
        return None

    def create_user(self, name: str, email: str, password: str, matricula: str, tipo_permissao: int):
        hashed_password = bcrypt.hash(password)

        with db.connect("create_user") as conn:
            try:
                with conn.cursor() as cursor:
                    query = """
                        INSERT INTO usuario (nome, email, senha, matricula, tipo_permissao)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING *
                    """
                    
                    cursor.execute(query, (name, email, hashed_password, matricula, tipo_permissao))
                    user = cursor.fetchone()
                    return user
            except psycopg2.Error as e:
                logging.error(f"Erro ao criar usuário: {e}")
                return None
    

