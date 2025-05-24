# config.py
import os

# Získá absolutní cestu ke složce, kde se nachází tento soubor
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Definice cesty k SQLite databázi – ta bude uložena v souboru users.db ve stejné složce
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')

    # Vypne sledování změn objektů – jinak by SQLAlchemy zobrazovalo varování
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Tajný klíč – potřebný např. pro zabezpečení formulářů nebo sessiony
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zalozni-klic'
    #SECRET_KEY = 'toto-je-nahodny-klic-pro-flask'
