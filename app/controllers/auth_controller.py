from flask import request, jsonify
import uuid
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from flask_babel import gettext as _

def sign_up():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        public_id=str(uuid.uuid4()),
        name=data['name'],
        role=data['role'],
        email=data['email'],
        password=hashed_password,
        phone=data['phone']
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": _("User-register-success.")}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": _("El correo electrónico ya está registrado.")}), 400

def sign_in():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token_expiration = timedelta(minutes=15)
        access_token = create_access_token(identity=user.public_id, expires_delta=token_expiration, additional_claims={'language': user.language})
        return jsonify({"message": _("Login exitoso"), "access_token": access_token}), 200
    else:
        return jsonify({"message": _("Credenciales incorrectas")}), 401

@jwt_required()
def current_user():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(public_id=current_user_id ).first()
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"msg": "User not found"}), 404
   
