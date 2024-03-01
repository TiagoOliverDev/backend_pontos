from .db import Db
import logging
import psycopg2

db = Db()

class JourneyRepository():

    def journey_exists(self, tipo: str):
        try:
            with db.connect("journey_exists") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT tipo FROM turno WHERE tipo = %s"
                    cursor.execute(query, (tipo,))
                    journey = cursor.fetchone()
                    return journey[0] if journey else None
        except psycopg2.Error as e:
            logging.error(f"Erro ao verificar se o setor existe: {e}")
            return None

    def update_journey(self, id: int, new_name: str):
        try:
            with db.connect("journey_edit") as conn:
                with conn.cursor() as cursor:
                    query = "UPDATE turno SET tipo = %s WHERE id_turno = %s"
                    cursor.execute(query, (new_name, id))
                    conn.commit()  
                    return True
        except psycopg2.Error as e:
            logging.error(f"Erro ao editar o nome do turno: {e}")
            return False

    def journey_create(self, tipo: str):
        try:
            with db.connect("journey_create") as conn:
                with conn.cursor() as cursor:
                    query = "INSERT INTO turno (tipo) VALUES (%s) RETURNING id_turno"
                    cursor.execute(query, (tipo,))
                    new_journey_id = cursor.fetchone()[0]
                    conn.commit()  
                    return new_journey_id
        except psycopg2.Error as e:
            logging.error(f"Erro ao cadastrar o turno: {e}")
            return None
        
    def journey_delete(self, id: int):
        try:
            with db.connect("journey_delete") as conn:
                with conn.cursor() as cursor:
                    query = "DELETE FROM turno WHERE id_turno = %s"
                    cursor.execute(query, (id,))
                    conn.commit()  
                    return True
        except psycopg2.Error as e:
            logging.error(f"Erro ao excluir o turno: {e}")
            return False
        
    def list_all_journeys(self):
        try:
            with db.connect("list_all_journeys") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT id_turno, tipo FROM turno"
                    cursor.execute(query)
                    journeys_tuples = cursor.fetchall()
                    journeys = [
                        {"id": sector[0], "tipo": sector[1]}
                        for sector in journeys_tuples if sector
                    ]
                    return journeys
        except psycopg2.Error as e:
            logging.error(f"Erro ao listar os turnos: {e}")
            return None
        
    def list_journey_by_id(self, id: int):
        try:
            with db.connect("list_journey_by_id") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT id_turno, tipo FROM turno WHERE id_turno = %s"
                    cursor.execute(query, (id,))
                    journey = cursor.fetchone()
                    return journey, None
        except psycopg2.Error as e:
            logging.error(f"Error listing journey by id: {e}")
            return None, 'Error listing journey by id. Please try again later.'
        
    def set_jorney(self, id_turno: int, id_usuario: int):
        try:
            with db.connect("set_jorney") as conn:
                with conn.cursor() as cursor:
                    query = "INSERT INTO usuario_turno (id_turno, id_usuario) VALUES (%s, %s) RETURNING id_vinculo_turno"
                    cursor.execute(query, (id_turno, id_usuario))
                    new_journey_id = cursor.fetchone()[0]
                    conn.commit()  
                    return new_journey_id
        except psycopg2.Error as e:
            logging.error(f"Erro ao cadastrar o turno: {e}")
            return None


