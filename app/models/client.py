from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID, ENUM
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime, timezone



client_type_enum = ENUM('individual', 'company', name='client_type_enum', create_type=True)
identification_type_enum = ENUM('RNC', 'NIF', 'Passport', 'Identity', name='identification_type_enum', create_type=True)

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    client_type = db.Column(client_type_enum, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=True) 
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    identification_type = db.Column(identification_type_enum, nullable=True)
    identification_number = db.Column(db.String(50), nullable=True)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.public_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __init__(self, client_type, name,first_name, last_name, email,created_by, phone=None, address=None, city=None, state=None, country=None, postal_code=None, identification_type=None, identification_number=None):
        self.client_type = client_type
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
        self.created_by = created_by
        self.identification_type = identification_type
        self.identification_number = identification_number

    def to_dict(self):
        return {
            'public_id': self.public_id,
            'client_type': self.client_type,
            'name': self.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code,
            'identification_type': self.identification_type,
            'identification_number': self.identification_number,
            'created_by': self.created_by,
            'created_at': self.created_at,
            'updated_at': self.updated_at
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
