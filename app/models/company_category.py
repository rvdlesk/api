# /app/models/company_category.py
from app import db
from flask_sqlalchemy import SQLAlchemy


class CompanyCategory(db.Model):
    __tablename__ = 'company_categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
