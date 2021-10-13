
import plotly.express as px
import pandas as pd
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

data = {'Product': ['Fuchka', 'Nachos', 'Baklava', 'Mug Dal', 'Paratha', 'Borhani', 'Ice Lime', 'Chotpoti', 'Extra Egg', 'Lava Cake'],
        'Amount': [5000, 6500, 8500, 7500, 6000, 9000, 10000, 8200, 9300, 9800]
        }
pdf = pd.DataFrame(data)

top_sale = html.Div([
    html.H1('Product Wise Sale(Top 10)', style={'textAlign': 'center'}),
    dcc.Graph(id='bargraph', figure=px.bar(pdf, x='Product', y='Amount', color='Product'))
])