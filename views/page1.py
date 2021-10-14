
# Dash packages
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from app import app


###############################################################################
########### LANDING PAGE LAYOUT ###########
###############################################################################
layout = dbc.Container([

        html.H2('Welcome to Dashboard'),
        html.Hr(),

], className="mt-4")