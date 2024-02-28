from flask import Blueprint

from .auth import auth_blueprint


routes_blueprint = Blueprint("routes", __name__)

routes_blueprint.register_blueprint(auth_blueprint)


