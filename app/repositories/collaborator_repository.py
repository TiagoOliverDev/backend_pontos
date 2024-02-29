from .db import Db
import logging
import psycopg2

db = Db()

class CollaboratorRepository():

    def collaborator_exists(self, name: str):
        try:
            with db.connect("collaborator_exists") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT nome FROM setor WHERE nome = %s"
                    cursor.execute(query, (name,))
                    collaborator = cursor.fetchone()
                    return collaborator[0] if collaborator else None
        except psycopg2.Error as e:
            logging.error(f"Erro ao verificar se o setor existe: {e}")
            return None

    def update_collaborator(self, id: int, new_name: str):
        try:
            with db.connect("setor_edit") as conn:
                with conn.cursor() as cursor:
                    query = "UPDATE setor SET nome = %s WHERE id_setor = %s"
                    cursor.execute(query, (new_name, id))
                    conn.commit()  
                    return True
        except psycopg2.Error as e:
            logging.error(f"Erro ao editar o nome do setor: {e}")
            return False

    def collaborator_create(self, name: str):
        try:
            with db.connect("collaborator_create") as conn:
                with conn.cursor() as cursor:
                    query = "INSERT INTO setor (nome) VALUES (%s) RETURNING id_setor"
                    cursor.execute(query, (name,))
                    new_collaborator_id = cursor.fetchone()[0]
                    conn.commit()  
                    return new_collaborator_id
        except psycopg2.Error as e:
            logging.error(f"Erro ao cadastrar o setor: {e}")
            return None
        
    def collaborator_delete(self, id: int):
        try:
            with db.connect("collaborator_delete") as conn:
                with conn.cursor() as cursor:
                    query = "DELETE FROM setor WHERE id_setor = %s"
                    cursor.execute(query, (id,))
                    conn.commit()  
                    return True
        except psycopg2.Error as e:
            logging.error(f"Erro ao excluir o setor: {e}")
            return False
        
    def list_all_collaborators(self):
        try:
            with db.connect("list_all_collaborators") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT id_setor, nome FROM setor"
                    cursor.execute(query)
                    collaborators = cursor.fetchall()
                    return collaborators
        except psycopg2.Error as e:
            logging.error(f"Erro ao listar os setores: {e}")
            return None
        
    def list_collaborator_by_id(self, id: int):
        try:
            with db.connect("list_collaborator_by_id") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT id_setor, nome FROM setor WHERE id_setor = %s"
                    cursor.execute(query, (id,))
                    collaborator = cursor.fetchone()
                    return collaborator, None
        except psycopg2.Error as e:
            logging.error(f"Error listing collaborator by id: {e}")
            return None, 'Error listing collaborator by id. Please try again later.'
        

