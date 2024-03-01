from ..repositories.collaborator_repository import CollaboratorRepository
import logging


collaborator_repository = CollaboratorRepository()

class CollaboratorService:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        
    def list_all_collaborators(self):
        try:
            collaborators = collaborator_repository.list_all_collaborators()
            if collaborators is None:
                return {'message': 'Error fetching collaborators'}, 500
            return collaborators, 200
        except Exception as e:
            logging.error(f"Error fetching collaborators: {e}")
            return {'message': 'Internal server error'}, 500
        
    def register_collaborator(self, name: str, email: str, password: str, matricula: str, tipo_permissao: int):
        try:
            if collaborator_repository.collaborator_email_exists(email):
                return None, 'email collaborator already exists'
            
            if collaborator_repository.collaborator_matricula_exists(matricula):
                return None, 'matricula collaborator already exists'

            collaborator_created = collaborator_repository.collaborator_create(name, email, password, matricula, tipo_permissao)
            return collaborator_created, None
        except Exception as e:
            logging.error(f"Error registering collaborator: {e}")
            return None, 'Error registering collaborator. Please try again later.'
    
    def list_collaborator_by_id(self, id: int):
        try:
            collaborator = collaborator_repository.list_collaborator_by_id(id=id)
            return collaborator, None
        except Exception as e:
            logging.error(f"Error list collaborator: {e}")
            return None, 'Error list collaborator. Please try again later.'
    
    def collaborator_update(self, id: int, **kwargs):
        try:
            collaborator_edited = collaborator_repository.update_collaborator(id=id, **kwargs)
            return collaborator_edited, None
        except Exception as e:
            logging.error(f"Error edit collaborator: {e}")
            return None, 'Error edit collaborator. Please try again later.'
        
    def collaborator_delete(self, id: int):
        try:
            collaborator_excluded = collaborator_repository.collaborator_delete(id=id)
            return collaborator_excluded, None
        except Exception as e:
            logging.error(f"Error in excluded collaborator: {e}")
            return None, 'Error in excluded collaborator. Please try again later.'

