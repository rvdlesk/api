from flask import abort, request, jsonify
from app.models import Client, User
from app import db, bcrypt 
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_babel import lazy_gettext as _l

@jwt_required()
def register_client():

    user = User.query.filter_by(public_id=get_jwt_identity()).first()
    if not user:
            return jsonify({"error": "User not found"}), 404
    claims = get_jwt()
    company_id = claims.get('company_id')
    created_by = user.id
    client_type = request.json.get('client_type')
    email = request.json.get('email')
    phone_prefix = request.json.get('phone_prefix')
    phone = request.json.get('phone')
    address = request.json.get('address')
    city = request.json.get('city')
    state = request.json.get('state')
    country = request.json.get('country')
    postal_code = request.json.get('postal_code')
    identification_type = request.json.get('identification_type')
    identification_number = request.json.get('identification_number')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    name = request.json.get('name')


    if not client_type or not email or not created_by:
        return jsonify({"msg": "Missing required fields"}), 400

    if client_type not in ['individual', 'company']:
        return jsonify({"msg": "Invalid client_type"}), 400

    if identification_type and identification_type not in ['RNC', 'NIF', 'Passport', 'Identity']:
        return jsonify({"msg": "Invalid identification_type"}), 400
    
    if not first_name or not last_name:
            return jsonify({"msg": "Missing first_name or last_name for individual client"}), 400

    if not name:
            return jsonify({"msg": "Missing name for company client"}), 400
      
        
    new_client = Client(
            client_type=client_type,
            email=email,
            name="",
            created_by=created_by,
            first_name=first_name,
            last_name=last_name,
            phone_prefix=phone_prefix,
            phone=phone,
            address=address,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code,
            identification_type=identification_type,
            identification_number=identification_number,
            company_id=company_id
    )
    try:
        db.session.add(new_client)
        db.session.commit()
        return jsonify({"msg": "Client created successfully", "public_id": new_client.public_id}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"details": str(e)}), 500
    
    
@jwt_required()
def get_all_clients():
    clients = Client.query.all()
    message = _l('Clients retrieved successfully')
    return {
        "message": message,
        "status": 200,
        "data": [client.to_dict() for client in clients]
    }