# /app/utils/validators.py
import re
from sqlalchemy.orm import validates

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
