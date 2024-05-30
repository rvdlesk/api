import os
import secrets
class Config:
    SQLALCHEMY_DATABASE_URI =  'postgresql://postgres:@localhost/mali_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'es'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    BABEL_SUPPORTED_LOCALES = ['en', 'es']
    JWT_SECRET_KEY = 'ox7zsvqwYEt__NScgpRjWapg1M1iOXAyZYdiAgRAk7E'
    ITS_DANGEROUS_SECRECT_KEY = secrets.token_urlsafe(32)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = True  # Cambia esto al servidor SMTP que estés usando
    MAIL_PORT = 587  # El puerto que estés usando, 587 es común para TLS
    MAIL_USE_TLS = True  # Habilita TLS
    MAIL_USERNAME = 'audittriad@gmail.com'  # Tu correo electrónico
    MAIL_PASSWORD = 'mufxzcemnyzcataj'
