from flask import abort, request, jsonify
from app.models.client import Client
from app import db, bcrypt 
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_babel import lazy_gettext as _l

@jwt_required()
def register_client():

    created_by = get_jwt_identity()
    client_type = request.json.get('client_type')
    email = request.json.get('email')
    phone = request.json.get('phone')
    address = request.json.get('address')
    city = request.json.get('city')
    state = request.json.get('state')
    country = request.json.get('country')
    postal_code = request.json.get('postal_code')
    identification_type = request.json.get('identification_type')
    identification_number = request.json.get('identification_number')
    
    if not client_type or not email or not created_by:
        return jsonify({"msg": "Missing required fields"}), 400

    if client_type not in ['individual', 'company']:
        return jsonify({"msg": "Invalid client_type"}), 400

    if identification_type and identification_type not in ['RNC', 'NIF', 'Passport', 'Identity']:
        return jsonify({"msg": "Invalid identification_type"}), 400

    if client_type == 'individual':
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        if not first_name or not last_name:
            return jsonify({"msg": "Missing first_name or last_name for individual client"}), 400
        new_client = Client(
            client_type=client_type,
            email=email,
            name="",
            created_by=created_by,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code,
            identification_type=identification_type,
            identification_number=identification_number
        )
    else:
        name = request.json.get('name')
        if not name:
            return jsonify({"msg": "Missing name for company client"}), 400
        new_client = Client(
            client_type=client_type,
            email=email,
            created_by=created_by,
            name=name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code,
            identification_type=identification_type,
            identification_number=identification_number
        )
    
    db.session.add(new_client)
    db.session.commit()
    
    return jsonify({"msg": "Client created successfully", "public_id": new_client.public_id}), 201

@jwt_required()
def get_all_clients():
    clients = Client.query.all()
    message = _l('Clients retrieved successfully')
    return {
        "message": message,
        "status": 200,
        "data": [client.to_dict() for client in clients]
    }