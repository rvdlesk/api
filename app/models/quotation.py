# app/models/quotation.py

from app import db
from app.helpers.validators import validate_and_clean_html
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from datetime import datetime, timezone


class Quotation(db.Model):
    __tablename__ = 'quotations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('quotations', lazy=True))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('quotations', lazy=True))
    amount = db.Column(db.Numeric, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)  # Relación con Currency
    currency = db.relationship('Currency', backref=db.backref('quotations', lazy=True))
    status = db.Column(db.String(50), nullable=False)  # Ejemplo: 'pending', 'accepted', 'rejected'
    valid_until = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('quotations', lazy=True))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            'public_id': self.public_id,
            'client_id': self.client.public_id,
            'company_id': self.company.public_id,
            'amount': self.amount,
            'currency': self.currency.to_dict(),  # Incluye información de la moneda
            'status': self.status,
            'valid_until': self.valid_until,
            'created_by': self.creator.public_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'items': [item.to_dict() for item in self.items]
        }


class QuotationItem(db.Model):
    __tablename__ = 'quotation_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    quotation = db.relationship('Quotation', backref=db.backref('items', lazy=True))
    description = db.Column(db.Text, nullable=False)  # Cambiado a Text para soportar HTML
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric, nullable=False)
    total = db.Column(db.Numeric, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    @validates('description')
    def validate_description(self, key, description):
        return validate_and_clean_html(description)

    def to_dict(self):
        return {
            'description': self.description,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total': self.total,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
class QuoteConfig(db.Model):
    __tablename__ = 'quote_config'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('quote_config', lazy=True))
    prefix = db.Column(db.String(20), nullable=True)  # Prefijo personalizado
    suffix = db.Column(db.String(20), nullable=True)  # Sufijo personalizado
    use_year = db.Column(db.Boolean, default=True, nullable=False)  # Incluir el año
    use_month = db.Column(db.Boolean, default=False, nullable=False)  # Incluir el mes
    sequential_number = db.Column(db.Integer, default=1, nullable=False)  # Número secuencial inicial
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)  # Moneda por defecto
    currency = db.relationship('Currency', backref=db.backref('quote_configs', lazy=True))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('quote_configs', lazy=True))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f'<QuoteConfig {self.prefix} - {self.suffix} - {self.sequential_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'prefix': self.prefix,
            'suffix': self.suffix,
            'use_year': self.use_year,
            'use_month': self.use_month,
            'sequential_number': self.sequential_number,
            'currency_id': self.currency_id,
            'created_by': self.created_by,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
