from flask import Blueprint, jsonify
from app.models.csv_model import CSVData

bp = Blueprint('bd_check', __name__)

@bp.route('/bdCheck')
def bd_check():
    try:
        count = CSVData.query.count()
        return jsonify({'message': 'OK!', 'count': count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500