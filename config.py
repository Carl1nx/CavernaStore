import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-padrao'

    # Lê os dados montados do .env
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Rotas configuráveis via variáveis de ambiente
    ROUTE_HO = os.environ.get('ROUTE_HO', '/')
    ROUTE_PROD = os.environ.get('ROUTE_PROD', '/produto')
    ROUTE_CAR = os.environ.get('ROUTE_CAR', '/carrinho')
    ROUTE_ADMIN = os.environ.get('ROUTE_ADMIN', '/admin')
    ROUTE_B = os.environ.get('ROUTE_B', '/admin/produto/deletar/<int:id>')