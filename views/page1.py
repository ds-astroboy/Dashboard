
# Dash packages
import dash_bootstrap_components as dbc
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
# import dash_html_components as html

from app import app


###############################################################################
########### LANDING PAGE LAYOUT ###########
###############################################################################
layout = dbc.Container([

        html.H2('Page 1 Layout badruzzaman Zamira'),
        html.Hr(),


], className="mt-4")
