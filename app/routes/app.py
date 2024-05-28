from flask import Blueprint, jsonify, request
from flask_babel import _

bp_app = Blueprint('app', __name__)

@bp_app.route('/', methods=['GET'])
def home():
    return "bienvendio"


