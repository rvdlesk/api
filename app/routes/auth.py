from flask import Blueprint
from app.controllers.auth_controller import sign_in, sign_up, current_user, validate_email, request_reset_password, reset_password

bp_auth = Blueprint('auth', __name__)

bp_auth.route('/signup', methods=['POST'])(sign_up)
bp_auth.route('/login', methods=['POST'])(sign_in)
bp_auth.route('/current', methods=['GET'])(current_user)
bp_auth.route('/validate_email/<token>', methods=['GET'])(validate_email)
bp_auth.route('/request_reset_password', methods=['POST'])(request_reset_password)
bp_auth.route('/reset_password/<token>', methods=['GET', 'POST'])(reset_password)
