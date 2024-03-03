# service.py

from ..repositories.reports_repository import ReportsRepository
import logging


reports_repository = ReportsRepository()

class ReportsService:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        
    def list_points_history_from_user(self, id_usuario: int):
        try:
            points_history = reports_repository.list_points_history_from_user(id_usuario=id_usuario)
            if points_history is None:
                return {'message': 'Error fetching points history'}, 500
            return points_history, 200
        except Exception as e:
            logging.error(f"Error fetching points history: {e}")
            return {'message': 'Internal server error'}, 500
        


        

