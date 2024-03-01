# service.py
from passlib.hash import bcrypt
from ..repositories.sector_repository import SectorRepository
import jwt
import logging


sector_repository = SectorRepository()

class SectorService:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        
    def list_all_sectors(self):
        try:
            sectors = sector_repository.list_all_sectors()
            if sectors is None:
                return None, 'Error fetching sectors'
            # formatted_sectors = self.format_sectors_all(sectors)
            # return formatted_sectors, None
            return sectors, None
        except Exception as e:
            logging.error(f"Error fetching sectors: {e}")
            return None, 'Internal server error'

    def format_sectors_all(self, sectors):
        formatted_sectors = []
        for sector in sectors:
            formatted_sector = {
                "id": sector[0],
                "nomeSetor": sector[1],
                "created_at": sector[2].strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "updated_at": sector[3].strftime("%a, %d %b %Y %H:%M:%S GMT")
            }
            formatted_sectors.append(formatted_sector)
        return formatted_sectors
        
    def register_sector(self, name: str):
        try:
            if sector_repository.sector_exists(name=name):
                return None, 'Sector already exists'

            sector_created = sector_repository.sector_create(name=name)
            return sector_created, None
        except Exception as e:
            logging.error(f"Error registering sector: {e}")
            return None, 'Error registering sector. Please try again later.'
    
    def list_sector_by_id(self, id: int):
        try:
            sector, error = sector_repository.list_sector_by_id(id=id)
            return sector, None
        except Exception as e:
            logging.error(f"Error list sector: {e}")
            return None, 'Error list sector. Please try again later.'
    
    def update_sector(self, id: int, name: str):
        try:
            sector_edited = sector_repository.update_sector(id=id, new_name=name)
            return sector_edited, None
        except Exception as e:
            logging.error(f"Error edit sector: {e}")
            return None, 'Error edit sector. Please try again later.'
        
    def sector_delete(self, id: int):
        try:
            sector_excluded = sector_repository.sector_delete(id=id)
            return sector_excluded, None
        except Exception as e:
            logging.error(f"Error in excluded sector: {e}")
            return None, 'Error in excluded sector. Please try again later.'

