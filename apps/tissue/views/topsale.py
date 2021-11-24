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
    # dbc.Container([
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns _01"), width=12, xs=6, style={'color': 'red'}),
                dbc.Col(html.Div("One of three columns _02"), width=12, xs=6, style={'color': 'red'}),
                dbc.Col(html.Div("One of three columns _03"), width=12, xs=6, style={'color': 'red'}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of four columns1"), width=6, lg=3, style={'color': 'red'}),
                dbc.Col(html.Div("One of four columns2"), width=6, lg=3, style={'color': 'red'}),
                dbc.Col(html.Div("One of four columns3"), width=6, lg=3, style={'color': 'red'}),
                dbc.Col(html.Div("One of four columns4"), width=6, lg=3, style={'color': 'red'}),
            ]
        ),
    # ])

])
