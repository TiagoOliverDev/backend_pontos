from .db import Db
from passlib.hash import bcrypt
from datetime import datetime
import logging
import psycopg2

db = Db()

class PointRepository():

    def create_user_point(self, id_usuario: int, id_tipo_ponto: int, data_hora: str):
        try:
            datetime_obj = datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")

            with db.connect("create_user_point") as conn:
                with conn.cursor() as cursor:
                    query = """
                        INSERT INTO registro_ponto (id_usuario, id_tipo_ponto, data_hora)
                        VALUES (%s, %s, %s)
                        RETURNING *
                    """
                    cursor.execute(query, (id_usuario, id_tipo_ponto, datetime_obj))
                    point = cursor.fetchone()
                    return point
        except ValueError:
            logging.error("Formato de data e hora inválido. Use o formato 'YYYY-MM-DD HH:MM:SS'")
            return None
        except psycopg2.IntegrityError as e:
            logging.error(f"Erro de integridade ao criar ponto: {e}")
            return None
        except psycopg2.Error as e:
            logging.error(f"Erro ao criar ponto: {e}")
            return None
    
    def list_points_from_user(self, id_usuario: int):
        try:
            with db.connect("list_points_from_user") as conn:
                with conn.cursor() as cursor:
                    query = """
                            select rp.data_hora, (select u.nome from usuario u where rp.id_usuario = u.id_usuario ), tp.tipo, rp.id_tipo_ponto  from registro_ponto rp 
                            inner join  tipo_ponto tp on rp.id_tipo_ponto = tp.id_tipo_ponto where rp.id_usuario = %s order by rp.id_ponto ;
                        """
                    cursor.execute(query, (id_usuario,))
                    point_tuples = cursor.fetchall()
                    points = [
                        {
                            "dataHora": point[0].strftime("%d %b %Y / %H:%M:%S"),
                            "nome": point[1],
                            "tipoPonto": point[2],
                            "idTipoPonto": point[3]
                        }
                        for point in point_tuples if point
                    ]
                    return points, None
        except psycopg2.Error as e:
            logging.error(f"Error listing point by id: {e}")
            return None, 'Error listing point by id. Please try again later.'
        

    ######################## Métodos para cadastrar e listar tipo de ponto na tabela TIPO_PONTO ########################
    def create_type_point(self, tipo: str):
        try:
            with db.connect("create_type_point") as conn:
                with conn.cursor() as cursor:
                    query = """
                        INSERT INTO tipo_ponto (tipo)
                        VALUES (%s)
                        RETURNING *
                    """
                    cursor.execute(query, (tipo,))
                    type_point = cursor.fetchone()
                    return type_point
        except psycopg2.IntegrityError as e:
            logging.error(f"Erro de integridade ao cadastrar ponto: {e}")
            return None
        except psycopg2.Error as e:
            logging.error(f"Erro ao cadastrar ponto: {e}")
            return None

    def list_all_type_points(self):
        try:
            with db.connect("list_all_type_points") as conn:
                with conn.cursor() as cursor:
                    query = "SELECT * FROM tipo_ponto ORDER BY id_tipo_ponto"
                    cursor.execute(query)
                    points = cursor.fetchall()
                    return points
        except psycopg2.Error as e:
            logging.error(f"Erro ao listar os tipos de pontos: {e}")
            return None
        