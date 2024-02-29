from .db import Db
import logging
import psycopg2

db = Db()

class SectorRepository():

    def sector_exists(self, name: str):
        try:
            with db.connect("sector_exists") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT nome FROM setor WHERE nome = %s"
                    cursor.execute(query, (name,))
                    sector = cursor.fetchone()
                    return sector[0] if sector else None
        except psycopg2.Error as e:
            logging.error(f"Erro ao verificar se o setor existe: {e}")
            return None

    def update_sector(self, id: int, new_name: str):
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

    def sector_create(self, name: str):
        try:
            with db.connect("sector_create") as conn:
                with conn.cursor() as cursor:
                    query = "INSERT INTO setor (nome) VALUES (%s) RETURNING id_setor"
                    cursor.execute(query, (name,))
                    new_sector_id = cursor.fetchone()[0]
                    conn.commit()  
                    return new_sector_id
        except psycopg2.Error as e:
            logging.error(f"Erro ao cadastrar o setor: {e}")
            return None
        
    def sector_delete(self, id: int):
        try:
            with db.connect("sector_delete") as conn:
                with conn.cursor() as cursor:
                    query = "DELETE FROM setor WHERE id_setor = %s"
                    cursor.execute(query, (id,))
                    conn.commit()  
                    return True
        except psycopg2.Error as e:
            logging.error(f"Erro ao excluir o setor: {e}")
            return False
        
    def list_all_sectors(self):
        try:
            with db.connect("list_all_sectors") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT id_setor, nome FROM setor"
                    cursor.execute(query)
                    sectors = cursor.fetchall()
                    return sectors
        except psycopg2.Error as e:
            logging.error(f"Erro ao listar os setores: {e}")
            return None
        
    def list_sector_by_id(self, id: int):
        try:
            with db.connect("list_sector_by_id") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT id_setor, nome FROM setor WHERE id_setor = %s"
                    cursor.execute(query, (id,))
                    sector = cursor.fetchone()
                    return sector, None
        except psycopg2.Error as e:
            logging.error(f"Error listing sector by id: {e}")
            return None, 'Error listing sector by id. Please try again later.'
        

