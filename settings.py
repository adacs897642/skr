# settings.py
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

FLASK_DEBUG = os.environ.get('FLASK_DEBUG')

POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_URL = os.environ.get('POSTGRES_URL')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PW = os.environ.get('POSTGRES_PW')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

# SECRET_KEY = os.environ.get("SECRET_KEY")
# DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
