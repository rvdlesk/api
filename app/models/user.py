# app/models/user.py
from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from ..helpers import validate_phone_prefix, validate_phone, validate_full_phone_number, validate_email
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column('name', db.String(100), nullable=False)
    role = db.Column('role', db.String(50), nullable=False)
    email = db.Column('email', db.String(120), nullable=False, unique=True)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    password = db.Column('password', db.String(128), nullable=False)
    phone_prefix = db.Column('phone_prefix',db.String(10), nullable=True)
    phone = db.Column('phone', db.String(15), nullable=False)
    language = db.Column(db.String(10), default='en')
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('users', lazy=True))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            'public_id': self.public_id,
            'company_id':self.company.public_id if self.company else None,
            'name': self.name,
            'role': self.role,
            'email': self.email,
            'phone_prefix': self.phone_prefix,
            'phone': self.phone
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
