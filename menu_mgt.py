from sqlalchemy import Table, ForeignKey
from sqlalchemy.sql import select
from config import engine, db
from sqlalchemy.orm import backref, relationship
from config import conn_security

class Menu(db.Model):
    MenuId = db.Column(db.Integer, primary_key=True)
    MenuName = db.Column(db.String(15))
    CompanyId = db.Column(db.Integer)

userTable = Table('menu', Menu.metadata)

def create_menu_table():
    Menu.metadata.create_all(engine)


def add_menu(menuname, company_id):
    insert_stmt = userTable.insert().values(
        MenuName= menuname,
        CompanyId= company_id
    )
    conn = engine.connect()
    conn.execute(insert_stmt)
    conn.close()


def update_menu(menu_id, menu_name):

    update = userTable.update().\
        values(rolename=menu_name).\
        where(userTable.c.Menu_Id == menu_id)

    conn = engine.connect()
    conn.execute(update)
    conn.close()

def show_menus():
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

def company_wise_menu(company_id = 0):
    menu_dropdown_data = []
    cursor = conn_security.cursor()
    sql = f"select r.MenuId, r.MenuName from Menu r where CompanyId = {company_id}"
    cursor.execute(sql)
    result = cursor.fetchall()
    _result = list(result)
    for index, item in _result:
        menu_dropdown_data.append({'id': index, 'MenuName': item})
    return menu_dropdown_data