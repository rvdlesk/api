from flask import Blueprint, jsonify, request
from app.controllers.user_controller import get_all_users, update_user, delete_user
from flask_babel import _
from flask_jwt_extended import jwt_required, get_jwt_identity

bp_user = Blueprint('users', __name__)

bp_user.route('/', methods=['GET'])(get_all_users)


@bp_user.route('/user/<int:id>', methods=['PUT'])
def modify_user(id):
    data = request.get_json()
    updated_user = update_user(id, data)
    return jsonify(updated_user.to_dict())

@bp_user.route('/user/<int:id>', methods=['DELETE'])
def remove_user(id):
    delete_user(id)
    return '', 204
