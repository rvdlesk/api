# app/models/currency.py

from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

class Currency(db.Model):
    __tablename__ = 'currencies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)  # Código de la moneda (e.g., USD, EUR)
    name = db.Column(db.String(50), nullable=False)  # Nombre de la moneda
    buy_rate = db.Column(db.Numeric, nullable=False)  # Tasa de compra
    sell_rate = db.Column(db.Numeric, nullable=False)  # Tasa de venta
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # Fecha y hora de última actualización
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            'public_id': self.public_id,
            'code': self.code,
            'name': self.name,
            'buy_rate': self.buy_rate,
            'sell_rate': self.sell_rate,
            'last_updated': self.last_updated,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
