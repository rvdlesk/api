# /app/utils/validators.py
import bleach
import re
from sqlalchemy.orm import validates
import datetime

def validate_phone_prefix(prefix):
    # Asegura que el prefijo comienza con un '+' opcional seguido de dígitos
    if prefix.startswith('+'):
        assert prefix[1:].isdigit(), "Phone prefix must contain only digits after '+'"
    else:
        assert prefix.isdigit(), "Phone prefix must contain only digits"
    
    # Verifica la longitud del prefijo
    assert 1 <= len(prefix) <= 5, "Phone prefix must be between 1 and 5 characters long"
    return prefix

def validate_phone(number):
    assert number.isdigit(), "Phone number must contain only digits"
    assert len(number) >= 7, "Phone number must be at least 7 digits long"
    return number

def validate_full_phone_number(instance, key, value):
    if key in ['phone', 'phone_prefix']:
        prefix = instance.phone_prefix if key == 'phone' else value
        phone = instance.phone if key == 'phone_prefix' else value
    elif key in ['phone2', 'phone2_prefix']:
        prefix = instance.phone2_prefix if key == 'phone2' else value
        phone = instance.phone2 if key == 'phone2_prefix' else value
    
    full_number = (prefix or '') + (phone or '')
    assert len(full_number) >= 10, "Full phone number (prefix + number) must be at least 10 digits long"
    return value

def validate_email(email):
    assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Invalid email address"
    return email


# Función de validación de HTML
ALLOWED_TAGS = ['b', 'i', 'u', 'a', 'p', 'ul', 'ol', 'li', 'br', 'span', 'div']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'span': ['style'],
    'div': ['style']
}

def validate_and_clean_html(html_content):
    """
    Limpia y valida contenido HTML permitiendo solo ciertas etiquetas y atributos.
    """
    return bleach.clean(html_content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)


def generate_number(config_type, company_id):
    from app import db
    from app.models import InvoiceConfig, QuoteConfig
    
    """
    Función genérica para generar números de invoice o quote.
    :param config_type: Tipo de configuración ('invoice' o 'quote')
    :param company_id: ID de la compañía
    :return: Número generado y la moneda por defecto
    """
    if config_type == 'invoice':
        config = InvoiceConfig.query.filter_by(company_id=company_id).first()
    elif config_type == 'quote':
        config = QuoteConfig.query.filter_by(company_id=company_id).first()
    else:
        raise ValueError("config_type must be 'invoice' or 'quote'")

    if not config:
        raise Exception(f"No {config_type} configuration found for the company.")

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    number_parts = []
    if config.prefix:
        number_parts.append(config.prefix)
    if config.use_year:
        number_parts.append(str(current_year))
    if config.use_month:
        number_parts.append(f'{current_month:02d}')
    number_parts.append(f'{config.sequential_number:04d}')
    if config.suffix:
        number_parts.append(config.suffix)

    config.sequential_number += 1
    db.session.commit()

    return '-'.join(number_parts), config.currency_id
