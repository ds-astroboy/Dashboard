
from config import conn_tissue
from common.settinginfo import *
import pandas as pd

#region Configuration Tissue

def get_all_marketchannels():
    cursor = conn_tissue.cursor()
    sql = f"select Id,Name from Market_Channels where MarketChannelType_Id = {division_type_id} " \
          f"and IsActive = 1 and BusinessLine_Id = {businessline_id} and Name not like '%Fake%' "
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def get_division_wise_areas(division_id = 0):
    cursor = conn_tissue.cursor()
    sql = f"select Id, Name from Market_Channels where Market_Channel_Id = {division_id}"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def get_all_child_marketchannels(marketchannel_id):
    # division_child_data = []
    cursor = conn_tissue.cursor()
    sql = f"select Id,Name from Market_Channels where Market_Channel_Id = {marketchannel_id} " \
          f"and IsActive = 1 and BusinessLine_Id = {businessline_id}  "
    cursor.execute(sql)
    result = cursor.fetchall()
    # for item in _result:
    #     division_child_data.append(item)
    return result

def get_all_partybusinessline_by_marketchannel(marketchannel_id):
    # partybusinessline_data = []
    cursor = conn_tissue.cursor()
    sql = f"select pb.Id, Party_Id, p.CompanyName as Name from Party_BusinessLines pb inner join parties p on p.Id = pb.Party_Id where pb.Market_Channel_Id = {marketchannel_id} " \
          f"and pb.IsActive = 1 and pb.BusinessLine_Id = {businessline_id}  "
    cursor.execute(sql)
    result = cursor.fetchall()
    # for item in _result:
    #     partybusinessline_data.append(item)
    return result

#endregion

#region Transactional information Tissue

# def get_partybusinessline_wise_stock(partybusinessline_id, start_date, end_date):
#     try:
#         sql = f'SprDashboardDistributorStock @BusinessLineId = {businessline_id}, @PartyBusinessLine_Id = {partybusinessline_id}' \
#               f',@FromDate= {start_date}, @ToDate = {end_date} '
#         df = pd.read_sql_query(sql, conn_tissue)
#         return df
#     except:
#         return "An exception occurred"

def get_all_marketchannel_stock(marketchannel_id,start_date, end_date):
    try:
        sql = f'SprDashboardDivisionStock @BusinessLineId = {businessline_id}, @MarketChannel_Id = {marketchannel_id}' \
              f',@FromDate= {start_date}, @ToDate = {end_date} '
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except:
        return "An exception occurred"

def get_secondary_sales_data(division_value, start_date, end_date):
    try:
        sql = f'SprDashboardSecondarySales @BusinessLineId = {businessline_id}, @MarketChannel_Id = {division_value}' \
              f',@FromDate= {start_date}, @ToDate = {end_date}'
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except:
        return {'value': -1}


def get_product_stock_data(division_value, start_date, end_date):
    try:
        sql = f'SprDashboardProductStock @BusinessLineId = {businessline_id}, @MarketChannel_Id = {division_value}' \
              f',@FromDate= {start_date}, @ToDate = {end_date} '
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except:
        return "An exception occurred"

def get_marketchannel_attendance_data(division_value, start_date, end_date):
    try:
        sql = f'SprDashboardAttendance @BusinessLineId = {businessline_id}, @MarketChannelId = {division_value}, ' \
              f'@FromDate = {start_date}, @ToDate = {end_date} '
        cursor = conn_tissue.cursor()
        cursor.execute(sql)
        conn_tissue.commit()

        df = pd.read_sql_query("select * from ##TempAttendance", conn_tissue)
        cursor.execute("drop table ##TempAttendance")
        cursor.commit()
        return df

    except ValueError:
        return ValueError

# def get_all_division_attendance_dash_data(start_date, end_date):
#     appended_data = []
#     try:
#         market_channels = get_all_marketchannels()
#         for item in market_channels:
#             # data = get_attendance_dash_data(item.Id, start_date, end_date)
#             # appended_data.append(data)
#         df = pd.concat(appended_data)
#         return df
#
#     except ValueError:
#         return ValueError

def get_executive_count_data(division_value = 0):
    try:
        sql = f'SprDashboardTotalExecutive @BusinessLineId = {businessline_id}, @MarketChannelId = {division_value}'
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except ValueError:
        return ValueError

def get_monthly_secondary_sales_data():
    try:
        sql = f'SprDashboardMonthlySecondarySales @BusinessLineId = {businessline_id}'
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except ValueError:
        return ValueError

def get_date_wise_secondary_sales_data(division_value, start_date, end_date):
    try:
        sql = f'SprDashboardDateWiseSecondarySales @BusinessLineId = {businessline_id},  @MarketChannelId = {division_value}, ' \
              f'@FromDate = {start_date}, @ToDate = {end_date} '
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except ValueError:
        return ValueError

def get_product_wise_secondary_sales_data(division_value, start_date, end_date):
    try:
        sql = f'SprDashboardProductWiseSecondarySales @BusinessLineId = {businessline_id},  @MarketChannelId = {division_value}, ' \
              f'@FromDate = {start_date}, @ToDate = {end_date} '
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except ValueError:
        return ValueError

def get_category_wise_secondary_sales_data(division_value, start_date, end_date):
    try:
        sql = f'SprDashboardCategoryWiseSecondarySales @BusinessLineId = {businessline_id},  @MarketChannelId = {division_value}, ' \
              f'@FromDate = {start_date}, @ToDate = {end_date} '
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except ValueError:
        return ValueError

#endregion
