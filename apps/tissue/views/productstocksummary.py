
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, dash_table, Input, Output
import pandas as pd


from app import app
from configuration.dropdown_mgt import get_divisions
from apps.tissue.model.models import get_sales_Dash_data, get_product_stock_dash_data
from common.dateinfo import *


division_values = get_divisions()
default_value = 0
for item in division_values[1].items():
    default_value = item[1]

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Product Stock Summary', className='card-header bg-success'),
                html.Div([
                    dbc.Row([
                        dbc.Col([], md=3),
                        dbc.Col([
                            dbc.Label('Division: '),
                            dcc.Dropdown(
                                id='division_dropdown',
                                style={
                                    'width': '90%'
                                },
                                options=division_values,
                                clearable=False,
                                value=default_value,
                            )], md=2),

                        dbc.Col([
                            dbc.Label('Start Date: '),
                            html.Div(style={'fontSize': 10},
                                     children=dcc.DatePickerSingle(
                                         id='start_date',
                                        date=start_day_of_prev_month
                                         # date='2021-07-01'
                                     ),
                                     )
                        ], md=2),
                        dbc.Col([
                            dbc.Label('End Date: '),
                            html.Div(style={'fontSize': 10},
                                     children=dcc.DatePickerSingle(
                                         id='end_date',
                                         date=last_day_of_prev_month
                                     ),
                                     )
                        ], md=2),
                        dbc.Col([

                        ], md=1),
                    ]),
                ], className='card-body')
            ], className='card bg-light mb-3', style={'text-align': 'center'})
        ], md=12),
        # dbc.Col([
        # ], md=1),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Overall Sales Order', className='card-header bg-info'),
            ], style={'text-align': 'center'}),
            html.Div([dash_table.DataTable(id='datasummary', data=[],)], style={'font-weight': 'bold'})
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Order by product category', className='card-header bg-info'),
                dcc.Graph(id='bargraph_product_category', figure={})], style={'text-align': 'center'})
        ], md=4),
        dbc.Col([
            html.Div([
                html.H4('Order by party', className='card-header bg-info'),
                dcc.Graph(id='bargraph_stock_party', figure={})], style={'text-align': 'center'})
        ], md=4),
        dbc.Col([
            html.Div([
                html.H4('Stock by product category', className='card-header bg-info'),
                dcc.Graph(id='bargraph_stock_category', figure={})], style={'text-align': 'center'})
        ], md=4),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Stock Status Table', className='card-header bg-info'),
            ], style={'text-align': 'left'}),
            dash_table.DataTable(id='dataproduct',
                                 data=[],
                                 fixed_rows={'headers': True},
                                 style_table={'height': 400}
                                 )
        ])
    ])
])


@app.callback(
    Output('bargraph_product_category', 'figure'),
    Output('bargraph_stock_party', 'figure'),
    Output('bargraph_stock_category', 'figure'),
    Output('datasummary', 'columns'),
    Output('datasummary', 'data'),
    Output('dataproduct', 'columns'),
    Output('dataproduct', 'data'),
    Input('division_dropdown', 'value'),
    Input('start_date', 'date'),
    Input('end_date', 'date'),
)
def update_salesorder_graph(division_dropdown_value, start_date, end_date):
    figure_category = {}
    figure_product = {}
    figure_product_stock = {}
    summary_data = []
    # Stock
    df5 = get_product_stock_dash_data(division_dropdown_value, start_date, end_date)
    # Sales
    df2 = get_sales_Dash_data(division_dropdown_value, start_date, end_date)
    if not df2.empty:

        # Order by product category
        df3 = df2.groupby(["ProductCategoryName"], as_index=False)["TotalOrderQty"].sum()
        figure_category = px.bar(df3, x='ProductCategoryName', y='TotalOrderQty', color="ProductCategoryName", height=300)

        # Order by Party
        df4 = df2.groupby(["PartyName"], as_index=False)["TotalOrderQty", "RemainingQty"].sum().head(20)
        figure_product = px.pie(df4, names='PartyName', values='TotalOrderQty', color="PartyName", height=300)

        # Stock by product category
        df6 = df5.groupby(["ProductCategoryName"], as_index=False)["CurrentStock"].sum()
        figure_product_stock = px.bar(df6, x="ProductCategoryName", y="CurrentStock", color="ProductCategoryName", height=300)

        order_count = df2["Code"].nunique()
        total_sales_amount = df2["TotalOrderPrice"].sum()
        total_order_qty = df2["TotalOrderQty"].sum()
        total_remaining_qty = df2["RemainingQty"].sum()

        summary_data.append({"Total Order": order_count,
                                     "Total Sales Amount": '{0:.2f}'.format(total_sales_amount),
                                     "Total Order Qty": '{0:.2f}'.format(total_order_qty),
                                     "Total Remaining Qty": '{0:.2f}'.format(total_remaining_qty)
                                     })
        df_table = pd.DataFrame(summary_data)
        df_product_stock_summary = df5[["ProductName", "OpeningStock", "ReceivedQty", "DeliveredQty", "CurrentStock"]]

    return figure_category, figure_product, figure_product_stock,\
           [{"name": i, "id": i} for i in df_table.columns], df_table.to_dict('records'),\
           [{"name": i, "id": i} for i in df_product_stock_summary.columns], df_product_stock_summary.to_dict('records')