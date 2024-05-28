import os

class Config:
    SQLALCHEMY_DATABASE_URI =  'postgresql://postgres:@localhost/mali_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'es'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    BABEL_SUPPORTED_LOCALES = ['en', 'es']
    JWT_SECRET_KEY = 'ox7zsvqwYEt__NScgpRjWapg1M1iOXAyZYdiAgRAk7E'
