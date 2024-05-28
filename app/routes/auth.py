from flask import Blueprint
from app.controllers.auth_controller import sign_in, sign_up, current_user

bp_auth = Blueprint('auth', __name__)

bp_auth.route('/register', methods=['POST'])(sign_up)
bp_auth.route('/login', methods=['POST'])(sign_in)
bp_auth.route('/current', methods=['GET'])(current_user)

