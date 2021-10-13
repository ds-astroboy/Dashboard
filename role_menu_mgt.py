from sqlalchemy import Table, ForeignKey
from sqlalchemy.sql import select
from config import engine, db
from sqlalchemy.orm import backref, relationship
from config import conn_security

class RoleMenu(db.Model):
    RoleMenuId = db.Column(db.Integer, primary_key=True)
    RoleId = db.Column(db.Integer)
    MenuId = db.Column(db.Integer)
    CompanyId = db.Column(db.Integer)
    CreateBy = db.Column(db.Integer)

userTable = Table('rolemenu', RoleMenu.metadata)

def create_role_menu_table():
    RoleMenu.metadata.create_all(engine)

def add_role_menu(company_id, role_id, menu_ids):
    cursor = conn_security.cursor()
    for menu_id in menu_ids:
        sql = f"select top(1) RoleMenuId from RoleMenu where RoleId = {role_id} and MenuId = {menu_id} and CompanyId = {company_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            conn = engine.connect()
            conn.execute("insert RoleMenu (RoleId,MenuId,CompanyId, IsActive) values(?,?,?,?)", role_id, menu_id, company_id, 1)
            conn.close()

def update_role_menu(role_id, role_name):

    update = userTable.update().\
        values(rolename=role_name).\
        where(userTable.c.RoleId == role_id)
    conn = engine.connect()
    conn.execute(update)
    conn.close()

def show_role_menus():
    role_menu_names = []
    cursor = conn_security.cursor()
    sql = "select r.RoleId, r.RoleName, c.CompanyName, r.CompanyId from role r inner join Company c on r.CompanyId =  c.CompanyId"
    cursor.execute(sql)
    result = cursor.fetchall()
    role_menus = list(result)
    for result in role_menus:
        role_menu_names.append({
            'RoleId': result[0],
            'MenuId': result[1],
            'CompanyId': result[2]
            })
    return role_menu_names