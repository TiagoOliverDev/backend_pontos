from .db import Db
from passlib.hash import bcrypt
import logging
import psycopg2

db = Db()

class CollaboratorRepository():

    def collaborator_email_exists(self, email: str):
        try:
            with db.connect("collaborator_exists") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT * FROM usuario WHERE email = %s"
                    cursor.execute(query, (email,))
                    collaborator = cursor.fetchone()
                    return collaborator[0] if collaborator else None
        except psycopg2.Error as e:
            logging.error(f"Erro ao verificar se o colaborador já existe pelo email: {e}")
            return None
        
    def collaborator_matricula_exists(self, matricula: str):
        try:
            with db.connect("collaborator_exists") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT * FROM usuario WHERE matricula = %s"
                    cursor.execute(query, (matricula,))
                    collaborator = cursor.fetchone()
                    return collaborator[0] if collaborator else None
        except psycopg2.Error as e:
            logging.error(f"Erro ao verificar se o colaborador já existe pela matricula: {e}")
            return None
        
    def collaborator_create(self, name: str, email: str, password: str, matricula: str, tipo_permissao: int):
        hashed_password = bcrypt.hash(password)

        with db.connect("create_user_comum") as conn:
            try:
                with conn.cursor() as cursor:
                    query = """
                        INSERT INTO usuario (nome, email, senha, matricula, tipo_permissao)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id_usuario
                    """
                    cursor.execute(query, (name, email, hashed_password, matricula, tipo_permissao))
                    user = cursor.fetchone()
                    return user
            except psycopg2.Error as e:
                logging.error(f"Erro ao criar usuário: {e}")
                return None
        
    def update_collaborator(self, id: int, **kwargs):
        # Extrai os campos atualizáveis do dicionário kwargs
        update_fields = {key: value for key, value in kwargs.items() if key in ['nome', 'email', 'senha', 'matricula']}

        if 'senha' in update_fields:
            update_fields['senha'] = bcrypt.hash(update_fields['senha'])

        # Constrói a query dinâmica para atualizar os campos
        set_clause = ', '.join([f"{field} = %s" for field in update_fields.keys()])
        values = tuple(update_fields.values()) + (id,)

        with db.connect("update_collaborator") as conn:
            try:
                with conn.cursor() as cursor:
                    query = f"""
                        UPDATE usuario
                        SET {set_clause}
                        WHERE id_usuario = %s
                        RETURNING *
                    """
                    cursor.execute(query, values)
                    user = cursor.fetchone()
                    return user
            except psycopg2.Error as e:
                logging.error(f"Error in updated collaborator: {e}")
                return None

    def collaborator_delete(self, id: int):
        try:
            with db.connect("collaborator_delete") as conn:
                with conn.cursor() as cursor:
                    query = "UPDATE usuario SET status = FALSE WHERE id_usuario = %s;"
                    cursor.execute(query, (id,))
                    conn.commit()  
                    return True
        except psycopg2.Error as e:
            logging.error(f"Erro ao excluir o usuario: {e}")
            return False
        
    def list_all_collaborators(self):
        try:
            with db.connect("list_all_collaborators") as conn:
                with conn.cursor() as cursor:
                    query = """
                        SELECT 
                            u.id_usuario, 
                            u.nome, 
                            u.email, 
                            u.matricula,
                            u.status,
                            (SELECT t.tipo FROM turno t WHERE t.id_turno = ut.id_turno) as tipo_turno,
                            (SELECT s.nome FROM setor s WHERE s.id_setor = us.id_setor) as nome_setor
                        FROM 
                            usuario u
                        LEFT JOIN 
                            usuario_turno ut ON u.id_usuario = ut.id_usuario
                        LEFT JOIN 
                            usuario_setor us ON u.id_usuario = us.id_usuario
                        WHERE u.status = true
                        ORDER BY u.id_usuario;
                    """
                    cursor.execute(query)
                    collaborator_tuples = cursor.fetchall()
                    collaborators = [
                        {
                            "id": collaborator[0],
                            "nome": collaborator[1],
                            "email": collaborator[2],
                            "matricula": collaborator[3],
                            "turno": collaborator[5],
                            "setor": collaborator[6]
                        }
                        for collaborator in collaborator_tuples if collaborator
                    ]
                    return collaborators
        except psycopg2.Error as e:
            logging.error(f"Erro ao listar os colaboradores: {e}")
            return None
        
    def list_collaborator_by_id(self, id: int):
        try:
            with db.connect("list_collaborator_by_id") as conn:
                with conn.cursor() as cursor:
                    query = """
                        SELECT 
                            u.id_usuario, 
                            u.nome, 
                            u.matricula,
                            u.email, 
                            u.senha,
                            (SELECT t.tipo FROM turno t WHERE t.id_turno = ut.id_turno) as tipo_turno,
                            (SELECT s.nome FROM setor s WHERE s.id_setor = us.id_setor) as nome_setor
                        FROM 
                            usuario u
                        INNER JOIN 
                            usuario_turno ut ON u.id_usuario = ut.id_usuario AND ut.id_usuario = %s
                        INNER JOIN 
                            usuario_setor us ON u.id_usuario = us.id_usuario AND us.id_usuario = %s
                    """
                    cursor.execute(query, (id,id))
                    collaborator_tuples = cursor.fetchall()
                    collaborators = [
                        {
                            "id": collaborator[0],
                            "nomeCompleto": collaborator[1],
                            "matricula": collaborator[2],
                            "email": collaborator[3],
                            "senha": collaborator[4],
                            "turno": collaborator[5],
                            "setor": collaborator[6]
                        }
                        for collaborator in collaborator_tuples if collaborator
                    ]
                    return collaborators
        except psycopg2.Error as e:
            logging.error(f"Error listing collaborator by id: {e}")
            return None, 'Error listing collaborator by id. Please try again later.'
        



