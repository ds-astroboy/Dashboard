
import pandas as pd
from config import *
from configuration.dropdown_mgt import get_all_divisions

def get_sales_Dash_data(division_value, start_date, end_date):
    try:
        start_date = "'{}'".format(start_date)
        end_date = "'{}'".format(end_date)
        if division_value is None:
            division_value = 0
        sql = f'SprSecondarySalesInfoDashboard @BusinessLineId = {businessline_id}, @MarketChannel_Id = {division_value}' \
              f',@FromDate= {start_date}, @ToDate = {end_date}'
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except:
        return "An exception occurred"


def get_product_stock_dash_data(division_value, start_date, end_date):
    try:
        start_date = "'{}'".format(start_date)
        end_date = "'{}'".format(end_date)
        if division_value is None:
            division_value = 0
        sql = f'SprProductDashboardStock @BusinessLineId = {businessline_id}, @MarketChannel_Id = {division_value}' \
              f',@FromDate= {start_date}, @ToDate = {end_date} '
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except:
        return "An exception occurred"

def get_attendance_dash_data(division_value, start_date, end_date):
    try:
        start_date = "'{}'".format(start_date)
        end_date = "'{}'".format(end_date)
        if division_value is None:
            division_value = 0

        sql = f'SprDashboardAttendance @BusinessLineId = {businessline_id}, @MarketChannelId = {division_value}, ' \
              f'@FromDate = {start_date}, @ToDate = {end_date} '
        cursor = conn_tissue.cursor()
        cursor.execute(sql)
        conn_tissue.commit()

        df = pd.read_sql_query("select * from ##Temp", conn_tissue)
        cursor.execute("drop table ##Temp")
        cursor.commit()

        return df

    except ValueError:
        return ValueError

def get_all_division_attendance_dash_data(start_date, end_date):
    appended_data = []
    try:
        market_channels = get_all_divisions()
        for item in market_channels:
            data = get_attendance_dash_data(item.Id, start_date, end_date)
            appended_data.append(data)
        df = pd.concat(appended_data)
        return df

    except ValueError:
        return ValueError

def get_executive_count_dash_data(division_value = 0):

    try:
        sql = f'SprDashboardTotalExecutive @BusinessLineId = {businessline_id}, @MarketChannelId = {division_value}'
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except ValueError:
        return ValueError

# def get_executive_attendance_count_dash_data(division_value, start_date, end_date):
#
#     try:
#         start_date = "'{}'".format(start_date)
#         end_date = "'{}'".format(end_date)
#
#         sql = f'SprDashboardAttendanceStatus @BusinessLineId = {businessline_id}, @MarketChannelId = {division_value}, ' \
#               f'@FromDate = {start_date}, @ToDate = {end_date} '
#         cursor = conn_tissue.cursor()
#
#         df = pd.read_sql_query("select * from ##tempStatus", conn_tissue)
#         cursor.execute("drop table ##tempStatus")
#         return df
#
#     except ValueError:
#         return ValueError

