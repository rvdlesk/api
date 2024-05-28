# app/models/user.py
from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'  # Nombre de la tabla en español

    id = db.Column('id', db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column('name', db.String(100), nullable=False)
    role = db.Column('role', db.String(50), nullable=False)
    email = db.Column('email', db.String(120), nullable=False, unique=True)
    password = db.Column('password', db.String(128), nullable=False)
    phone = db.Column('phone', db.String(15), nullable=False)
    language = db.Column(db.String(10), default='en')

    def to_dict(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'role': self.role,
            'email': self.email,
            'phone': self.phone
        }

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address, "Invalid email address"
        return address

    @validates('phone')
    def validate_phone(self, key, number):
        assert number.isdigit(), "Phone number must contain only digits"
        assert len(number) >= 10, "Phone number must be at least 10 digits long"
        return number