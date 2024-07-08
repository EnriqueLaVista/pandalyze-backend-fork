from flask import Blueprint

bp = Blueprint('health_check', __name__)

@bp.route('/healthCheck')
def index():
    return 'OK!'