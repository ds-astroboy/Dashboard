import configparser
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pyodbc

config = configparser.ConfigParser()
config.read('config.txt')
engine = create_engine(config.get('database', 'con'))

db = SQLAlchemy()

