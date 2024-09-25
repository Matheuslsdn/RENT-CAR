from app import db
from app import create_app

with create_app().app_context():
    db.create_all()
    print('Banco de dados criado com sucesso!')