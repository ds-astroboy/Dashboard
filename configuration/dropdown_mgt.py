
from config import *

def get_all_divisions():
    division_dropdown_data = []
    cursor = conn_tissue.cursor()
    sql = f"select Id,Name from Market_Channels where MarketChannelType_Id = {division_type_id} " \
          f"and IsActive = 1 and BusinessLine_Id = {businessline_id} and Name not like '%Fake%' "
    cursor.execute(sql)
    _result = cursor.fetchall()
    for item in _result:
        division_dropdown_data.append(item)
    return division_dropdown_data

def get_divisions():
    division_dropdown_data = []
    division_dropdown_data.append({'label': "ALL", 'value': 0})
    cursor = conn_tissue.cursor()
    sql = f"select Id,Name from Market_Channels where MarketChannelType_Id = {division_type_id} " \
          f"and IsActive = 1 and BusinessLine_Id = {businessline_id} and Name not like '%Fake%'"
    cursor.execute(sql)
    _result = cursor.fetchall()
    for index, item in _result:
        division_dropdown_data.append({'label': item, 'value':  int(index)})
    return division_dropdown_data

def division_wise_areas(division_id = 0):
    area_dropdown_data = []
    cursor = conn_tissue.cursor()
    sql = f"select Id, Name from Market_Channels where Market_Channel_Id = {division_id}"
    cursor.execute(sql)
    _result = cursor.fetchall()
    for index, item in _result:
        area_dropdown_data.append({'value': int(index), 'label': item})
    return area_dropdown_data

def area_wise_territory(area_id = 0):
    territory_dropdown_data = []
    cursor = conn_tissue.cursor()
    sql = f"select Id, Name from Market_Channels where Market_Channel_Id = {area_id}"
    cursor.execute(sql)
    _result = cursor.fetchall()
    for index, item in _result:
        territory_dropdown_data.append({'value': int(index), 'label': item})
    return territory_dropdown_data

def area_wise_parties(area_id = 0):
    party_dropdown_data = []
    cursor = conn_tissue.cursor()
    sql = f"select pr.Id, pr.CompanyName as Name from Party_BusinessLines p " \
          f"inner join Parties pr on p.Party_Id = pr.Id " \
          f"inner join Market_Channels t on p.Market_Channel_Id = t.Id where t.Id = {area_id} " \
          f"order by pr.CompanyName"
    cursor.execute(sql)
    _result = cursor.fetchall()
    for index, item in _result:
        party_dropdown_data.append({'Id': int(index), 'Name': item})
    return party_dropdown_data