# service.py
from passlib.hash import bcrypt
from ..repositories.point_repository import PointRepository
import jwt
import logging


point_repository = PointRepository()

class PointService:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        
    def create_user_point(self, id_usuario: int, id_tipo_ponto: int, data_hora: str):
        try:
            set_point = point_repository.create_user_point(id_usuario=id_usuario, id_tipo_ponto=id_tipo_ponto, data_hora=data_hora)
            return set_point, None
        except Exception as e:
            logging.error(f"Error in set point: {e}")
            return None, 'Error in set point. Please try again later.'
        
    def list_points_from_user(self, id_usuario: int):
        try:
            points = point_repository.list_points_from_user(id_usuario=id_usuario)
            if points is None:
                return {'message': 'Error fetching points'}, 500
            return points, 200
        except Exception as e:
            logging.error(f"Error fetching points: {e}")
            return {'message': 'Internal server error'}, 500
        
    def create_type_point(self, tipo: str):
        try:
            set_point = point_repository.create_type_point(tipo=tipo)
            return set_point, None
        except Exception as e:
            logging.error(f"Error in create type point: {e}")
            return None, 'Error in create type point. Please try again later.'

    def list_all_type_points(self):
        try:
            points = point_repository.list_all_type_points()
            if points is None:
                return {'message': 'Error fetching types points'}, 500
            return {'points': points}, 200
        except Exception as e:
            logging.error(f"Error fetching points: {e}")
            return {'message': 'Internal server error'}, 500

    def list_point_by_id(self, id: int):
        try:
            point = point_repository.list_point_by_id(id=id)
            return point, None
        except Exception as e:
            logging.error(f"Error list point: {e}")
            return None, 'Error list point. Please try again later.'
    
        
        

