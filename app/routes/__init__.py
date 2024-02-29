from flask import Blueprint
from .auth import auth_blueprint 
from .sector import sector_blueprint 
from .collaborator import collaborator_blueprint


routes_blueprint = Blueprint("routes", __name__)

routes_blueprint.register_blueprint(auth_blueprint)
routes_blueprint.register_blueprint(sector_blueprint)
routes_blueprint.register_blueprint(collaborator_blueprint)