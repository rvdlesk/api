import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_babel import Babel, gettext, lazy_gettext as _l
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request, exceptions
from config import Config
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
serializer = URLSafeTimedSerializer(Config.ITS_DANGEROUS_SECRECT_KEY)

def get_locale():
    try:
        verify_jwt_in_request(optional=True) 
        identity = get_jwt_identity()
        if identity:
            lang = identity.get('language')
            print(f"Detected language from JWT: {lang}")  # Agregar para depuración
            if lang in Config.BABEL_SUPPORTED_LOCALES:
                return lang
    except Exception as e:
        print(f"Error in get_locale: {e}")  # Agregar para depuración
    return Config.BABEL_DEFAULT_LOCALE

def create_app():
    app = Flask(__name__)
    babel = Babel(app)
    app.config.from_object(Config)
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Inicializa Babel dentro de create_app y asigna el selector de idioma
    babel.init_app(app, locale_selector=get_locale)

    from app.routes import register_blueprints
    register_blueprints(app)

    with app.app_context():
        from app.models import User, Client, Company, IndividualPosition, CompanyCategory, Token
        db.create_all()
    # Registro de manejadores de errores
    register_error_handlers(app)

    # Ruta para listar las rutas registradas
    @app.route('/routes')
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': ','.join(rule.methods),
                'rule': rule.rule
            })
        routes_info = "<br>".join([f"Endpoint: {route['endpoint']}, Methods: {route['methods']}, Rule: {route['rule']}" for route in routes])
        return routes_info


    @app.route('/test_access')
    def test_access():
        try:
            es_mo_path = os.path.join(app.root_path, 'translations', 'es', 'LC_MESSAGES', 'messages.mo')
            if os.path.exists(es_mo_path):
                return jsonify({"message": "File is accessible", "path": es_mo_path})
            else:
                return jsonify({"message": "File is not accessible", "path": es_mo_path}), 404
        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500

    
    @app.route('/translation')
    def test_translation():
        msg = _l(u"Users retrieved successfully")
        print(f"Detected locale: {get_locale()}")  # Agregar para depuración
        print(f"Translated message: {msg}")  # Agregar para depuración
        return jsonify({"message": msg})

    @app.route('/test_babel')
    def test_babel():
        current_locale = get_locale()
        translations = babel.list_translations()
        return jsonify({
            "current_locale": current_locale,
            "translations": [str(t) for t in translations]
    })

    return app



def register_error_handlers(app):
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        # Capturar detalles del error
        original_exception = error.orig
        if hasattr(original_exception, 'diag') and original_exception.diag.constraint_name:
            constraint = original_exception.diag.constraint_name
            # Puedes personalizar los mensajes según el constraint que falló
            if constraint == 'users_email_key':
                return jsonify({"error": "El correo electrónico ya está registrado."}), 400
        return jsonify({"error": "Error de integridad en la base de datos."}), 400
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": gettext("Resource not found")}), 404

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({"error": gettext("Bad request"),"msg":str(error)}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": gettext("Internal server error")}), 500
