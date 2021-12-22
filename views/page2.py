
# Dash packages
import dash_bootstrap_components as dbc
# import dash_html_components as html
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
from app import app

###############################################################################
########### PAGE 2 LAYOUT ###########
###############################################################################
layout = dbc.Container([

        html.H2('Page 2 Layout', style={"color":"red"}),
        html.Hr(),


], className="mt-4")
