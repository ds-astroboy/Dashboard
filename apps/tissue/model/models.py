
import pandas as pd
from config import *

def get_sales_Dash_data(division_value, start_date, end_date):
    try:
        start_date = "'{}'".format(start_date)
        end_date = "'{}'".format(end_date)
        if division_value is None:
            division_value = 0
        sql = f'SprSecondarySalesInfoDashboard @BusinessLineId = {businessline_id}, @MarketChannel_Id = {division_value}, @FromDate= {start_date}, @ToDate = {end_date}'
        df = pd.read_sql_query(sql, conn_tissue)
        return df
    except:
        return "An exception occurred"
