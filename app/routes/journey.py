from flask import request, jsonify, Blueprint
from ..repositories.journey_repository import JourneyRepository
from ..services.journey_service import JourneyService
from .validated_token import token_required
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
journey_service = JourneyService(SECRET_KEY)

journey_repository = JourneyRepository()

journey_blueprint = Blueprint("journey", __name__, url_prefix="/journey")


@journey_blueprint.route('/list_all_journeys', methods=['GET'])
@token_required
def list_all_journeys(current_user):
    journeys = journey_service.list_all_journeys()
    if journeys is None:
        return jsonify({'message': 'Error fetching journeys'}), 500
    
    return jsonify({'journeys': journeys}), 200

@journey_blueprint.route('/register_journey', methods=['POST'])
@token_required
def register_journey(current_user):
    data = request.get_json()
    tipo = data['tipo']
    
    if not all([tipo]):
        return jsonify({'message': 'Field is required'}), 400

    journey, error = journey_service.register_journey(tipo=tipo)
    if error:
        return jsonify({'message': error}), 400

    return jsonify({'journey': journey, 'message': 'journey created successfully'}), 201

@journey_blueprint.route('/journey/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def journey(current_user, id):
    if request.method == 'GET':
        journey, error = journey_service.list_journey_by_id(id=id)
        if error:
            return jsonify({'message': error}), 500
        if not journey:
            return jsonify({'message': 'journey not found'}), 404
        
        return jsonify({'journey': journey}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if 'name' not in data:
            return jsonify({'message': 'Name is required'}), 400

        name = data['name']

        updated_journey, error = journey_service.update_journey(id=id, name=name)
        if error:
            return jsonify({'message': error}), 500
        if not updated_journey:
            return jsonify({'message': 'journey not found'}), 404
        
        return jsonify({'journey': updated_journey}), 200

    elif request.method == 'DELETE':
        success, error = journey_service.journey_delete(id=id)
        if error:
            return jsonify({'message': error}), 500
        if not success:
            return jsonify({'message': 'journey not found'}), 404
        
        return jsonify({'message': 'journey deleted successfully'}), 200
    
@journey_blueprint.route('/set_journey', methods=['POST'])
@token_required
def set_journey(current_user):
    data = request.get_json()
    id_turno = data['id_turno']
    id_usuario = data['id_usuario']
    
    if not all([id_turno, id_usuario]):
        return jsonify({'message': 'Field is required'}), 400

    journey, error = journey_service.set_jorney(id_turno=id_turno, id_usuario=id_usuario)
    if error:
        return jsonify({'message': error}), 400

    return jsonify({'journey': journey, 'message': 'journey created successfully'}), 201
