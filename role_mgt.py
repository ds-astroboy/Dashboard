from sqlalchemy import Table, ForeignKey
from sqlalchemy.sql import select
from config import engine, db
from sqlalchemy.orm import backref, relationship
from config import conn_security

class Role(db.Model):
    RoleId = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.String(15))
    CompanyId = db.Column(db.Integer)

userTable = Table('role', Role.metadata)

def create_role_table():
    Role.metadata.create_all(engine)


def add_role(rolename, company_id):
    insert_stmt = userTable.insert().values(
        RoleName= rolename,
        CompanyId= company_id
    )
    conn = engine.connect()
    conn.execute(insert_stmt)
    conn.close()


def update_role(role_id, role_name):

    update = userTable.update().\
        values(rolename=role_name).\
        where(userTable.c.RoleId == role_id)

    conn = engine.connect()
    conn.execute(update)
    conn.close()

def show_roles():
    cursor = conn_security.cursor()
    sql = "select r.RoleId, r.RoleName, c.CompanyName, r.CompanyId from role r inner join Company c on r.CompanyId =  c.CompanyId"
    cursor.execute(sql)
    result = cursor.fetchall()
    role_names = list(result)
    roles = []
    for result in role_names:
        roles.append({
            'RoleId': result[0],
            'RoleName': result[1],
            'CompanyName': result[2]
            })
    return roles

def company_wise_role(company_id = 0):
    role_dropdown_data = []
    cursor = conn_security.cursor()
    sql = f"select r.RoleId, r.RoleName from Role r where r.CompanyId = {company_id}"
    cursor.execute(sql)
    result = cursor.fetchall()
    _result = list(result)
    for index, item in _result:
        role_dropdown_data.append({'RoleName': item, 'RoleId': index})
    return role_dropdown_data