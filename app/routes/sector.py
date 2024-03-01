from flask import request, jsonify, Blueprint
from ..repositories.sector_repository import SectorRepository
from ..services.sector_service import SectorService
from .validated_token import token_required
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
sector_service = SectorService(SECRET_KEY)

sector_repository = SectorRepository()

sector_blueprint = Blueprint("sector", __name__, url_prefix="/sector")


@sector_blueprint.route('/list_all_sectors', methods=['GET'])
@token_required
def list_all_sectors(current_user):
    sectors = sector_service.list_all_sectors()
    if sectors is None:
        return jsonify({'message': 'Error fetching sectors'}), 500
    
    return jsonify({'sectors': sectors}), 200


@sector_blueprint.route('/register_sector', methods=['POST'])
# @token_required
def register_sector():
    data = request.get_json()
    name = data['nomeSetor']

    print('name:', name)

    if not all([name]):
        return jsonify({'message': 'Field is required'}), 400

    sector, error = sector_service.register_sector(name=name)
    if error:
        return jsonify({'message': error}), 400

    return jsonify({'sector': sector, 'message': 'Sector created successfully'}), 201


@sector_blueprint.route('/sector/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def sector(current_user, id):
    if request.method == 'GET':
        sector, error = sector_service.list_sector_by_id(id=id)
        if error:
            return jsonify({'message': error}), 500
        if not sector:
            return jsonify({'message': 'Sector not found'}), 404
        
        return jsonify({'sector': [sector] if sector else [None]}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if 'nomeSetor' not in data:
            return jsonify({'message': 'nomeSetor is required'}), 400

        name = data['nomeSetor']

        updated_sector, error = sector_service.update_sector(id=id, name=name)
        if error:
            return jsonify({'message': error}), 500
        if not updated_sector:
            return jsonify({'message': 'Sector not found'}), 404
        
        return jsonify({'sector': updated_sector}), 200

    elif request.method == 'DELETE':
        success, error = sector_service.sector_delete(id=id)
        if error:
            return jsonify({'message': error}), 500
        if not success:
            return jsonify({'message': 'Sector not found'}), 404
        
        return jsonify({'message': 'Sector deleted successfully'}), 200