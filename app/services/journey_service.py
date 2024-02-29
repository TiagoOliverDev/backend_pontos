# service.py
from passlib.hash import bcrypt
from ..repositories.journey_repository import JourneyRepository
import jwt
import logging


journey_repository = JourneyRepository()

class JourneyService:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        
    def list_all_journeys(self):
        try:
            journeys = journey_repository.list_all_journeys()
            if journeys is None:
                return {'message': 'Error fetching journeys'}, 500
            return {'journeys': journeys}, 200
        except Exception as e:
            logging.error(f"Error fetching journeys: {e}")
            return {'message': 'Internal server error'}, 500
        
    def register_journey(self, tipo: str):
        try:
            if journey_repository.journey_exists(tipo=tipo):
                return None, 'journey already exists'

            journey_created = journey_repository.journey_create(tipo=tipo)
            return journey_created, None
        except Exception as e:
            logging.error(f"Error registering journey: {e}")
            return None, 'Error registering journey. Please try again later.'
    
    def list_journey_by_id(self, id: int):
        try:
            journey = journey_repository.list_journey_by_id(id=id)
            return journey, None
        except Exception as e:
            logging.error(f"Error list journey: {e}")
            return None, 'Error list journey. Please try again later.'
    
    def update_journey(self, id: int, name: str):
        try:
            journey_edited = journey_repository.update_journey(id=id, new_name=name)
            return journey_edited, None
        except Exception as e:
            logging.error(f"Error edit journey: {e}")
            return None, 'Error edit journey. Please try again later.'
        
    def journey_delete(self, id: int):
        try:
            journey_excluded = journey_repository.journey_delete(id=id)
            return journey_excluded, None
        except Exception as e:
            logging.error(f"Error in excluded journey: {e}")
            return None, 'Error in excluded journey. Please try again later.'
        
    def set_jorney(self, id_turno: int, id_usuario: int):
        try:
            set_journey = journey_repository.set_jorney(id_turno=id_turno, id_usuario=id_usuario)
            return set_journey, None
        except Exception as e:
            logging.error(f"Error in set journey: {e}")
            return None, 'Error in set journey. Please try again later.'

