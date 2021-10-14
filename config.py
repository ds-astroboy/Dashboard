import configparser
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pyodbc

config = configparser.ConfigParser()
config.read('config.txt')
engine = create_engine(config.get('database', 'con'))

db = SQLAlchemy()

# Security connection
conn_security = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EHGT2P0;'
                      'Database=DashSecurity;'
                      'Trusted_Connection=yes;')

# Tissue connection
server = '10.10.244.158'
database = 'SalesForceDB'
username = '11900054'
password = '11900054@Stage158.COM'
conn_tissue = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)