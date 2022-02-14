import configparser
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pyodbc

businessline_id = 3
division_type_id = 21
config = configparser.ConfigParser()
config.read('config.txt')
engine = create_engine(config.get('database', 'con'))

db = SQLAlchemy()

# Security connection
s_server = '10.10.83.69'
s_Database = 'DashSecurity'
s_username = 'sa'
s_password = 'Root@pass1'
conn_security = pyodbc.connect('DRIVER={SQL Server};SERVER='+s_server+';DATABASE='+s_Database+';UID='+s_username+';PWD='+s_password)

# Tissue connection
server = '10.10.244.158'
database = 'SalesForceDB'
username = '11900054'
password = '11900054'
conn_tissue = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)