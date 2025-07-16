from flask import Blueprint, jsonify
from app.models.csv_model import CSVData
from flask_cors import cross_origin

bp = Blueprint('bd_check', __name__)

@bp.route('/bdCheck')
@cross_origin()
def bd_check():
    try:
        count = CSVData.query.count()
        return jsonify({'message': 'OK!', 'count': count}), 200
    except Exception as e:
        from app import db
        db.create_all()
        CSVData.query.all()
        return jsonify({'message': e}), 200