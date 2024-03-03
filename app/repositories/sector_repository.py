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
                    query = "SELECT id_setor, nome, created_at, updated_at FROM setor ORDER BY id_setor"
                    cursor.execute(query)
                    sector_tuples = cursor.fetchall()
                    sectors = [
                        {"id": sector[0], "nomeSetor": sector[1], "created_at": sector[2].strftime("%d %b %Y / %H:%M:%S"), "updated_at": sector[3].strftime("%d %b %Y / %H:%M:%S"),}
                        for sector in sector_tuples if sector
                    ]
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
                    sector_tuple = cursor.fetchone()
                    if sector_tuple:
                        sector = {"id": sector_tuple[0], "nomeSetor": sector_tuple[1]}
                    else:
                        sector = None
                    return sector, None
        except psycopg2.Error as e:
            logging.error(f"Error listing sector by id: {e}")
            return None, 'Error listing sector by id. Please try again later.'
        
    def set_sector(self, id_setor: int, id_usuario: int):
        try:
            with db.connect("set_sector") as conn:
                with conn.cursor() as cursor:
                    query = "INSERT INTO usuario_setor (id_setor, id_usuario) VALUES (%s, %s) RETURNING id_vinculo_setor"
                    cursor.execute(query, (id_setor, id_usuario))
                    new_journey_id = cursor.fetchone()[0]
                    conn.commit()  
                    return new_journey_id
        except psycopg2.Error as e:
            logging.error(f"Erro ao cadastrar o setor: {e}")
            return None


