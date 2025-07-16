from flask import Blueprint
from flask_cors import cross_origin

bp = Blueprint('health_check', __name__)

@bp.route('/healthCheck')
@cross_origin()
def index():
    return 'OK!'