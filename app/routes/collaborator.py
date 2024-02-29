from flask import request, jsonify, Blueprint
from ..repositories.collaborator_repository import CollaboratorRepository
from ..services.collaborator_service import CollaboratorService
from .validated_token import token_required
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
collaborator_service = CollaboratorService(SECRET_KEY)

collaborator_repository = CollaboratorRepository()

collaborator_blueprint = Blueprint("collaborator", __name__, url_prefix="/collaborator")


@collaborator_blueprint.route('/list_all_collaborators', methods=['GET'])
@token_required
def list_all_collaborators(current_user):
    collaborators = collaborator_service.list_all_collaborators()
    if collaborators is None:
        return jsonify({'message': 'Error fetching collaborators'}), 500
    
    return jsonify({'collaborators': collaborators}), 200


@collaborator_blueprint.route('/register_collaborator', methods=['POST'])
@token_required
def register_collaborator(current_user):
    data = request.get_json()
    name = data['name']

    if not all([name]):
        return jsonify({'message': 'Field is required'}), 400

    collaborator, error = collaborator_service.register_collaborator(name=name)
    if error:
        return jsonify({'message': error}), 400

    return jsonify({'collaborator': collaborator, 'message': 'collaborator created successfully'}), 201


@collaborator_blueprint.route('/collaborator/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def collaborator(current_user, id):
    if request.method == 'GET':
        collaborator, error = collaborator_service.list_collaborator_by_id(id=id)
        if error:
            return jsonify({'message': error}), 500
        if not collaborator:
            return jsonify({'message': 'collaborator not found'}), 404
        
        return jsonify({'collaborator': collaborator}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if 'name' not in data:
            return jsonify({'message': 'Name is required'}), 400

        name = data['name']

        updated_collaborator, error = collaborator_service.update_collaborator(id=id, name=name)
        if error:
            return jsonify({'message': error}), 500
        if not updated_collaborator:
            return jsonify({'message': 'collaborator not found'}), 404
        
        return jsonify({'collaborator': updated_collaborator}), 200

    elif request.method == 'DELETE':
        success, error = collaborator_service.collaborator_delete(id=id)
        if error:
            return jsonify({'message': error}), 500
        if not success:
            return jsonify({'message': 'collaborator not found'}), 404
        
        return jsonify({'message': 'collaborator deleted successfully'}), 200