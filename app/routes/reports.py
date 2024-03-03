from flask import jsonify, Blueprint
from ..repositories.reports_repository import ReportsRepository
from ..services.reports_service import ReportsService
from .validated_token import token_required
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
reports_service = ReportsService(SECRET_KEY)

reports_repository = ReportsRepository()

reports_blueprint = Blueprint("reports", __name__, url_prefix="/reports")


@reports_blueprint.route('/all_points__history_from_user/<int:id>', methods=['GET'])
@token_required
def all_points__history_from_user(current_user, id):
    points = reports_service.list_points_history_from_user(id_usuario=id)
    if points is None:
        return jsonify({'message': 'Error fetching points history'}), 500
    
    return jsonify({'points history': points}), 200

