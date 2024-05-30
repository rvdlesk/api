# app/models/user.py
from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID, ENUM
from datetime import datetime, timezone
business_type_enum = ENUM('individual', 'company', name='business_type_enum', create_type=True)
identification_type_enum = ENUM('RNC', 'NIF', 'Passport', 'Identity', name='identification_type_enum_company', create_type=True)

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    identification_type = db.Column(identification_type_enum, nullable=True)
    identification_number = db.Column(db.String(50), nullable=True)
    employee_range = db.Column(db.String(50), nullable=False)  # Ejemplo: '1-10', '11-50', '51-200', etc.
    business_description = db.Column(db.Text, nullable=True)
    business_type = db.Column(business_type_enum, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('company_categories.id'), nullable=True)
    category = db.relationship('CompanyCategory', backref=db.backref('companies', lazy=True))
    position_id = db.Column(db.Integer, db.ForeignKey('individual_positions.id'), nullable=True)
    position = db.relationship('IndividualPosition', backref=db.backref('companies', lazy=True))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


    def to_dict(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'employee_range': self.employee_range,
            'business_description': self.business_description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
