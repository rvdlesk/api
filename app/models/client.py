from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID, ENUM
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime, timezone
from ..helpers import validate_phone_prefix, validate_phone, validate_full_phone_number, validate_email

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
    phone_prefix = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    identification_type = db.Column(identification_type_enum, nullable=True)
    identification_number = db.Column(db.String(50), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('clients', lazy=True))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('users', lazy=True))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            'public_id': self.public_id,
            'company_id':self.company.public_id if self.company else None,
            'client_type': self.client_type,
            'name': self.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_prefix': self.phone_prefix,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code,
            'identification_type': self.identification_type,
            'identification_number': self.identification_number,
            'created_by': self.creator.public_id if self.creator else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @validates('phone_prefix', 'phone')
    def validate_phone_attributes(self, key, value):
        if key in ['phone_prefix']:
            return validate_phone_prefix(value)
        elif key in ['phone']:
            value = validate_phone(value)
        return validate_full_phone_number(self, key, value)

    @validates('email')
    def validate_email(self, key, email):
        return validate_email(email)
