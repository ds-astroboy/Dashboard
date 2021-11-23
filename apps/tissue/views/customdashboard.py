
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from app import app
from configuration.dropdown_mgt import get_divisions, division_wise_areas, area_wise_territory, get_all_divisions
from apps.tissue.model.models import get_all_division_attendance_dash_data, get_executive_count_dash_data, get_sales_Dash_data
from common.dateinfo import *


layout = html.Div([
         html.Div([
             html.Header("this is a test page", style={'color': 'red'})
         ]),
    html.Div([

    ]),
    html.Div([

    ]),

], style={'display': 'flex', 'background-color': '#192444', 'margin': '5%'})



