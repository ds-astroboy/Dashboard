# import dash_core_components as dcc
# import dash_html_components as html
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import plotly.express as px
import pandas as pd
from config import conn_tissue

# sql = 'SprSecondarySalesInfoDashboard'
# df = pd.read_sql(sql, conn_tissue)
# crm_dash = html.Div([
#     html.H1('Category Wise Sale(Top 10)', style={'textAlign': 'center'}),
#     dcc.Graph(id='bargraph', figure=px.bar(df, x='ProductCategoryName', y='TotalOrderPrice', color='ProductCategoryName'))
# ])