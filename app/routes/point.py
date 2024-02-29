from flask import request, jsonify, Blueprint
from ..repositories.point_repository import PointRepository
from ..services.point_service import PointService
from .validated_token import token_required
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
point_service = PointService(SECRET_KEY)

point_repository = PointRepository()

point_blueprint = Blueprint("point", __name__, url_prefix="/point")


@point_blueprint.route('/all_points_from_user/<int:id>', methods=['GET'])
@token_required
def all_points_from_user(current_user, id):
    points = point_service.list_points_from_user(id_usuario=id)
    if points is None:
        return jsonify({'message': 'Error fetching points'}), 500
    
    return jsonify({'points': points}), 200

@point_blueprint.route('/create_point', methods=['POST'])
@token_required
def create_point(current_user):
    data = request.get_json()
    id_usuario = data['id_usuario']
    id_tipo_ponto = data['id_tipo_ponto']
    data_hora = data['data_hora']
    
    if not all([id_usuario, id_tipo_ponto, data_hora]):
        return jsonify({'message': 'Fields are required'}), 400

    point, error = point_service.create_user_point(id_usuario=id_usuario, id_tipo_ponto=id_tipo_ponto, data_hora=data_hora)
    if error:
        return jsonify({'message': error}), 400

    return jsonify({'point': point, 'message': 'point created successfully'}), 201

@point_blueprint.route('/type_point', methods=['GET','POST'])
@token_required
def type_point(current_user):
    if request.method == 'GET':
        points = point_service.list_all_type_points()
        if not points:
            return jsonify({'message': 'points not found'}), 404
        return jsonify({'points': points}), 200
    
    if request.method == 'POST':
        data = request.get_json()
        tipo = data['tipo']
        
        if not all([tipo]):
            return jsonify({'message': 'Field is required'}), 400

        point, error = point_service.create_type_point(tipo=tipo)
        if error:
            return jsonify({'message': error}), 400

        return jsonify({'point': point, 'message': 'type point created successfully'}), 201

