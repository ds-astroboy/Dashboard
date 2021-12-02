
from adapters.repository import *
import numpy as np

#region Configuration Tissue
def get_service_all_partybusinesslines(marketchannel_id=0):
    data = []
    if marketchannel_id > 0:
        result_child_MC = get_all_child_marketchannels(marketchannel_id)
        for _item in result_child_MC:
            result_party_info = get_all_partybusinessline_by_marketchannel(_item.Id)
            data.append(result_party_info)
        return data
    else:
        child_MC_data = []
        result_MC = get_all_marketchannels()
        for item in result_MC:
            result_child_MC = get_all_child_marketchannels(item[0])
            child_MC_data.append(result_child_MC)
        for _item in child_MC_data:
            for it in _item:
                result_party = get_all_partybusinessline_by_marketchannel(it[0])
                data.append(result_party)
        return data

def get_service_division_dropdown():
    data = []
    data.append({'label': "ALL", 'value': 0})
    result = get_all_marketchannels()
    for index, item in result:
        data.append({'label': item, 'value':  int(index)})
    return data

def get_service_division_wise_area_dropdown(division_id=0):
    data = []
    data.append({'label': "ALL", 'value': 0})
    result = get_division_wise_areas(division_id)
    for index, item in result:
        data.append({'label': item, 'value':  int(index)})
    return data


# def get_marketchannel_stock(marketchannel_id, start_date, end_date):
#     data = []
#     start_date = "'{}'".format(start_date)
#     end_date = "'{}'".format(end_date)
#     result_party_info = get_all_partybusinesslines(marketchannel_id)
#     for item in result_party_info:
#         result_stock = get_partybusinessline_wise_stock(item.Id,  start_date, end_date)
#         data.append(result_stock)
#     return data

#endregion

#region Transactional information Tissue

def get_service_marketchannel_stock(marketchannel_id, start_date, end_date):
    try:
        start_date = "'{}'".format(start_date)
        end_date = "'{}'".format(end_date)
        df = get_all_marketchannel_stock(marketchannel_id, start_date, end_date)
        return df
    except ValueError:
        return ValueError


def get_service_secondary_sales_data(division_value, start_date, end_date):
    try:
        start_date = "'{}'".format(start_date)
        end_date = "'{}'".format(end_date)
        if division_value is None:
            division_value = 0
        df = get_secondary_sales_data(division_value, start_date, end_date)
        return df
    except ValueError:
        return ValueError

def get_service_attendance_data(division_value, start_date, end_date):
    try:
        start_date = "'{}'".format(start_date)
        end_date = "'{}'".format(end_date)
        if division_value is None:
            division_value = 0
        df = get_marketchannel_attendance_data(division_value, start_date, end_date)
        return df
    except ValueError:
        return ValueError

def get_service_all_division_attendance_data(start_date, end_date):
    appended_data = []
    try:
        market_channels = get_all_marketchannels()
        for item in market_channels:
            data = get_service_attendance_data(item[0], start_date, end_date)
            appended_data.append(data)
        df = pd.concat(appended_data)
        return df
    except ValueError:
        return ValueError

def get_service_executive_count_data(division_value = 0):
    try:
        df = get_executive_count_data(division_value)
        return df
    except ValueError:
        return ValueError

def get_service_product_stock_data(division_value, start_date, end_date):
    try:
        start_date = "'{}'".format(start_date)
        end_date = "'{}'".format(end_date)
        if division_value is None:
            division_value = 0
        df = get_product_stock_data(division_value, start_date, end_date)
        df['CurrentStock'] = df['CurrentStock'].apply(np.floor)
        return df
    except:
        return "An exception occurred"

#endregion

