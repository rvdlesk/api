from flask import Blueprint

def register_blueprints(app):
    
    from app.routes.user import bp_user
    from app.routes.auth import bp_auth
    from app.routes.client import bp_client
    
    app.register_blueprint(bp_user, url_prefix='/users')
    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_client, url_prefix='/clients')
    
