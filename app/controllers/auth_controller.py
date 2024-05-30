from flask import request, jsonify, url_for, render_template
from flask_mail import Message
import uuid
from app import db, bcrypt, mail, serializer
from app.models import User, Company, Token
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from flask_babel import gettext as _

def sign_up():
    data = request.get_json()
    
    # Validar entrada de datos
    required_fields = ['name', 'email', 'password', 'phone', 'role', 'company_name', 'employee_range', 'business_type']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": _(f"El campo {field} es requerido.")}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Validar identificación
    if data['business_type'] == 'individual':
        if 'position_id' not in data:
            return jsonify({"error": _("El campo position_id es requerido para individuos.")}), 400
        new_company = Company(
            public_id=str(uuid.uuid4()),
            name=data['company_name'],
            employee_range=data['employee_range'],
            business_type= data['business_type'],
            position_id=data['position_id']
        )
    else:
        if 'category_id' not in data:
            return jsonify({"error": _("El campo category_id es requerido para empresas.")}), 400
        new_company = Company(
            public_id=str(uuid.uuid4()),
            name=data['company_name'],
            business_type= data['business_type'],
            employee_range=data['employee_range'],
            category_id=data['category_id']
        )

    new_user = User(
        public_id=str(uuid.uuid4()),
        name=data['name'],
        role=data['role'],
        email=data['email'],
        password=hashed_password,
        phone_prefix=data['phone_prefix'],
        phone=data['phone'],
    )
    
    try:
        db.session.add(new_company)
        db.session.flush()  # Asegura que new_company obtenga un ID antes de continuar
        new_user.company_id = new_company.id  # Asigna el company_id al usuario
        db.session.add(new_user)
        db.session.commit()
        
        # Enviar correo de validación
        token = serializer.dumps(new_user.email, salt='email-confirm')
        validation_link = url_for('auth.validate_email', token=token, _external=True)
        html = render_template('email_validation.html', name=new_user.name, validation_link=validation_link)
        msg = Message('Validate your email', sender='audittriad@gmail.com', recipients=[new_user.email], html=html)
        mail.send(msg)
        
        return jsonify({"message": "User registered. Please check your email to validate your account."}), 201
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"details": str(e)}), 500


def validate_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)  # Token válido por 1 hora
        user = User.query.filter_by(email=email).first_or_404()

        if user.email_verified:
            return jsonify({"message": "Email is already validated."}), 200

        user.email_verified = True
        db.session.commit()
        return jsonify({"message": "Email successfully validated."}), 200
    except Exception as e:
        return jsonify({"error": "Invalid or expired token.", "details": str(e)}), 400
    
def sign_in():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token_expiration = timedelta(minutes=15)
        access_token = create_access_token(identity=user.public_id, expires_delta=token_expiration, additional_claims={'language': user.language,'company_id':user.company_id})
        return jsonify({"message": _("Login exitoso"), "access_token": access_token}), 200
    else:
        return jsonify({"message": _("Credenciales incorrectas")}), 401


def request_reset_password():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        token = serializer.dumps(user.email, salt='password-reset')
        reset_link = url_for('auth.reset_password', token=token, _external=True)
        html = render_template('password_reset.html', name=user.name, reset_link=reset_link)
        msg = Message('Reset your password', sender='audittriad@gmail.com', recipients=[user.email], html=html)
        mail.send(msg)

         # Guardar el token en la base de datos
        new_token = Token(token=token, email=user.email)
        db.session.add(new_token)
        db.session.commit()
        
        return jsonify({"message": "Please check your email for a password reset link."}), 200
    else:
        return jsonify({"error": "Email not found."}), 404


def reset_password(token):
    if request.method == 'GET':
        try:
            email = serializer.loads(token, salt='password-reset', max_age=3600)
            # Verificar si el token ha sido usado
            token_entry = Token.query.filter_by(token=token).first()
            if token_entry and token_entry.used:
                return jsonify({"error": "This reset link has already been used."}), 400
        except Exception as e:
            return jsonify({"error": "Invalid or expired token.", "details": str(e)}), 400
        return render_template('reset_password.html', token=token)

    data = request.form
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
        user = User.query.filter_by(email=email).first_or_404()
        
        # Verificar si el token ha sido usado
        token_entry = Token.query.filter_by(token=token).first()
        if token_entry and token_entry.used:
            return jsonify({"error": "This reset link has already been used."}), 400

        # Restablecer la contraseña y marcar el token como usado
        hashed_password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
        user.password = hashed_password
        token_entry.used = True
        db.session.commit()
        return jsonify({"message": "Password successfully reset."}), 200
    except Exception as e:
        return jsonify({"error": "Invalid or expired token.", "details": str(e)}), 400

@jwt_required()
def current_user():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(public_id=current_user_id ).first()
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"msg": "User not found"}), 404
   
