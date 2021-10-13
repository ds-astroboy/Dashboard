from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import select
from config import engine, db, conn_security


class Company(db.Model):
    CompanyId = db.Column(db.Integer, primary_key=True)
    CompanyShortName = db.Column(db.String(15))
    CompanyName = db.Column(db.String(15))
    # role = relationship("Role", back_populates="company", uselist=False)
    # Role = relationship("role", back_populates="company", uselist=False)

userTable = Table('company', Company.metadata)

def show_companies():
    companies = []
    select_stmt = select([userTable.c.CompanyId,
                        userTable.c.CompanyShortName,
                        userTable.c.CompanyName
                        ])
    conn = engine.connect()
    results = conn.execute(select_stmt)
    for result in results:
        companies.append({
            'CompanyId': result[0],
            'CompanyShortName': result[1],
            'CompanyName': result[2]
            })
    conn.close()
    return companies

def company_dropdown():
    company_dropdown_data = []
    result = show_companies()
    for item in result:
        company_dropdown_data.append({'label': item['CompanyName'], 'value': item['CompanyId']})
    return company_dropdown_data