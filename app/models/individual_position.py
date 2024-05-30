# /app/models/individual_position.py
from app import db
from flask_sqlalchemy import SQLAlchemy


class IndividualPosition(db.Model):
    __tablename__ = 'individual_positions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
