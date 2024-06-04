from app import db
from app.helpers.validators import validate_and_clean_html
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from datetime import datetime, timezone


class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('invoices', lazy=True))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('invoices', lazy=True))
    amount = db.Column(db.Numeric, nullable=False)
    subtotal = db.Column(db.Numeric, nullable=False)  # Subtotal de la factura
    itbis_percentage = db.Column(db.Numeric, nullable=True)  # Porcentaje de ITBIS
    itbis_amount = db.Column(db.Numeric, nullable=True)  # Monto de ITBIS calculado
    total = db.Column(db.Numeric, nullable=False)  # Total de la factura
    tax_reference_number = db.Column(db.String(50), nullable=True)
    issued_with_tax_reference = db.Column(db.Boolean, default=False, nullable=False)  # Indica si la factura se emite con comprobante fiscal
    is_void = db.Column(db.Boolean, default=False, nullable=False)  # Indica si la factura está anulada
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)  # Relación con Currency
    currency = db.relationship('Currency', backref=db.backref('quotations', lazy=True))
    status = db.Column(db.String(50), nullable=False)  # Ejemplo: 'unpaid', 'paid', 'cancelled'
    due_date = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('invoices', lazy=True))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            'public_id': self.public_id,
            'client_id': self.client.public_id,
            'company_id': self.company.public_id,
            'subtotal': self.subtotal,
            'itbis_percentage': self.itbis_percentage,
            'itbis_amount': self.itbis_amount,
            'total': self.total,
            'currency': self.currency.to_dict(),  # Incluye información de la moneda
            'tax_reference_number': self.tax_reference_number,
            'issued_with_tax_reference': self.issued_with_tax_reference,
            'status': self.status,
            'due_date': self.due_date,
            'created_by': self.creator.public_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'items': [item.to_dict() for item in self.items]
        }

class InvoiceItem(db.Model):
    __tablename__ = 'invoice_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    invoice = db.relationship('Invoice', backref=db.backref('items', lazy=True))
    description = db.Column(db.String(255), nullable=False)
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

class InvoiceConfig(db.Model):
    __tablename__ = 'invoice_config'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('invoice_config', lazy=True))
    prefix = db.Column(db.String(20), nullable=True)  # Prefijo personalizado
    suffix = db.Column(db.String(20), nullable=True)  # Sufijo personalizado
    use_year = db.Column(db.Boolean, default=True, nullable=False)  # Incluir el año
    use_month = db.Column(db.Boolean, default=False, nullable=False)  # Incluir el mes
    sequential_number = db.Column(db.Integer, default=1, nullable=False)  # Número secuencial inicial
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)  # Moneda por defecto
    currency = db.relationship('Currency', backref=db.backref('invoice_configs', lazy=True))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('invoice_configs', lazy=True))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f'<InvoiceConfig {self.prefix} - {self.suffix} - {self.sequential_number}>'

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
    
