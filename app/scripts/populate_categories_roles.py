# /app/scripts/populate_categories_roles.py

#script para ejecutarlo:
# python -m app.scripts.populate_categories_roles

from app import create_app, db
from app.models.company_category import CompanyCategory
from app.models.individual_position import IndividualPosition

def populate_categories_roles():
    company_categories = [
        {"name": "Technology", "description": "Companies in the technology sector"},
        {"name": "Healthcare", "description": "Companies in the healthcare sector"},
        {"name": "Finance", "description": "Companies in the finance sector"},
        # Agrega más categorías según sea necesario
    ]

    individual_positions = [
        {"name": "Entrepreneur", "description": "Individuals who are entrepreneurs"},
        {"name": "Accountant", "description": "Individuals who are accountants"},
        {"name": "Programmer", "description": "Individuals who are programmers"},
        {"name": "Designer", "description": "Individuals who are designers"},
        # Agrega más roles según sea necesario
    ]

    for category_data in company_categories:
        category = CompanyCategory(name=category_data["name"], description=category_data.get("description"))
        db.session.add(category)

    for role_data in individual_positions:
        role = IndividualPosition(name=role_data["name"], description=role_data.get("description"))
        db.session.add(role)

    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate_categories_roles()
