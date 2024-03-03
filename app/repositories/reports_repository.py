from .db import Db
import logging
import psycopg2

db = Db()

class ReportsRepository():

    def list_points_history_from_user(self, id_usuario: int):
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
        
