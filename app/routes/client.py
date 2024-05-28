from flask import Blueprint
from app.controllers.client_controller import register_client , get_all_clients

bp_client= Blueprint('clients', __name__)

bp_client.route('/', methods=['POST'])(register_client)
bp_client.route('/', methods=['GET'])(get_all_clients)

