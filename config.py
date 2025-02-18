import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'segredo'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///livraria.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False