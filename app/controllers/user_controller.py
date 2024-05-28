from flask import abort
from app.models.user import User
from app import db, bcrypt 
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_babel import lazy_gettext as _l


@jwt_required()
def get_all_users():
    users = User.query.all()
    message = _l('Users retrieved successfully')
    return {
        "message": message,
        "status": 200,
        "data": [user.to_dict() for user in users]
    }

def update_user(user_id, data):
    user = User.query.get_or_404(user_id)
    user.name = data.get('name', user.name)
    user.role = data.get('role', user.role)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    
    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
