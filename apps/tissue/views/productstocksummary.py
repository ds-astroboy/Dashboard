
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output
import plotly.graph_objs as go

from app import app
from common.dateinfo import *
from service_layer.services import get_service_division_dropdown, get_service_product_stock_data

default_value = 0
division_values = get_service_division_dropdown()
default_value = division_values[1]['value']

layout = html.Div([

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Product Stock', style={'fontSize': 30}),
               ], className='text-white', style={'text-align': 'center'})
        ]),
    ]),

    dbc.Row([
        # dbc.Col([
        # ], md=1),
        dbc.Col([
            html.Div([
                html.Div([
                    dbc.Row([
                        dbc.Col([], md=3),
                        dbc.Col([
                            dbc.Label('Division: ', color="white"),
                            dcc.Dropdown(
                                id='division_stock_dropdown',
                                style={
                                    'width': '90%',
                                },
                                options=division_values,
                                clearable=False,
                                value=default_value,
                            )], md=2),
                        dbc.Col([
                            dbc.Label('Start Date: ', color="white"),
                            html.Div(style={'fontSize': 10},
                                     children=dcc.DatePickerSingle(
                                         id='start_date',
                                         date=start_day_of_prev_month
                                     ),
                                     )
                        ], md=2),
                        dbc.Col([
                            dbc.Label('End Date: ', color="white"),
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
                ], className='')
            ], className='create_container', style={'text-align': 'center'})
        ], md=12),
        # dbc.Col([
        # ], md=1),
    ]),

    dbc.Row([
        dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                        dcc.Graph(id='category_pie', figure={})
                        ], className="create_container")
                    ]),
                ], className="text-white"),
        ], md=3, style={'text-align': 'center'}),

        dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                        dcc.Graph(id='product_bar', figure={})
                        ], className="create_container")
                    ]),
                ], className="text-white"),
        ], md=9, style={'text-align': 'center'}),
    ]),

     # dbc.Row([
     #           # https://hexcolor.co/hex/1f2c56    Color picker
     #            dbc.Col([
     #              html.Div([
     #                html.Div([
     #                    html.H4('Category Stock Info', style={'color': 'white'}),
     #                  ], style={'text-align': 'left'}),
     #                dash_table.DataTable(id='category_stock',
     #                                     data=[],
     #                                     fixed_rows={'headers': True},
     #                                     style_table={'height': 400},
     #                                     style_header={
     #                                            'backgroundColor': '#1f2c56',
     #                                             'color': 'white',
     #                                              'fontWeight': 'bold'
     #                                                },
     #                                     style_data_conditional=[{
     #                                         'if': {'column_editable': False},
     #                                         'backgroundColor': '#1f2c56',
     #                                         'color': 'white'
     #                                     }],
     #                                     )
     #            ], className="create_container"),
     #            ], md=4, style={'text-align': 'center'}),
     #     dbc.Col([
     #         html.Div([
     #             html.Div([
     #                 html.H4('Product Stock Info', style={'color': 'white'}),
     #             ], style={'text-align': 'left'}),
     #             dash_table.DataTable(id='product_stock',
     #                                  data=[],
     #                                  fixed_rows={'headers': True},
     #                                  style_table={'height': 400},
     #                                  style_header={
     #                                      'backgroundColor': '#1f2c56',
     #                                      'color': 'white',
     #                                      'fontWeight': 'bold'
     #                                  },
     #                                  style_data_conditional=[{
     #                                      'if': {'column_editable': False},
     #                                      'backgroundColor': '#1f2c56',
     #                                      'color': 'white',
     #                                  }],
     #                                  )
     #         ], className="create_container"),
     #        ], md=8, style={'text-align': 'center'})
     #        ])
])


@app.callback(
    Output('category_pie', 'figure'),
    Output('product_bar', 'figure'),
    # Output('category_stock', 'columns'),
    # Output('category_stock', 'data'),
    # Output('product_stock', 'columns'),
    # Output('product_stock', 'data'),


    Input('start_date', 'date'),
    Input('end_date', 'date'),
    Input('division_stock_dropdown', 'value')
)

def update_product_dashboard(start_date, end_date, division_dropdown_value):

    df = get_service_product_stock_data(start_date, end_date, division_dropdown_value)
    if not df.empty:
        df_stock = df.sort_values(by=["CurrentStock"],  ascending=False).head(150)
        category_grouped_df = df.groupby(["ProductCategoryName"], as_index=False)["CurrentStock"].sum().sort_values('CurrentStock',  ascending=False).head(15)
        # category_colors = ['#37F04D', '#3798FA', '#CE67E0', '#F79A65', '#F0E427', '#37B0F0', '#FADD36', '#CE67E0', '#65F799', '#EDA061',  'orange']
        category_wise_stock_data = {
            'data': [go.Bar(x=category_grouped_df['ProductCategoryName'],
                            y=category_grouped_df['CurrentStock'],
                            # name='',
                            marker=dict(color='#37C2FA'),
                            # hoverinfo='text',
                            # hovertext=''

                            ),
                     # go.Scatter(x=category_grouped_df['ProductCategoryName'],
                     #            y=category_grouped_df['CurrentStock'],
                     #            mode='lines',
                     #            name='',
                     #            line=dict(width=3, color='#FF00FF'),
                     #            marker=dict(
                     #                color='green'),
                     #            hoverinfo='text',
                     #            hovertext=''
                     #            )
                     ],

            'layout': go.Layout(
                plot_bgcolor='#1f2c56',
                paper_bgcolor='#1f2c56',
                title={
                    'text': 'Category',
                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'white',
                    'size': 20},

                hovermode='x',
                margin=dict(r=0),
                xaxis=dict(title='Category',
                           color='white',
                           showline=True,
                           showgrid=True,
                           showticklabels=True,
                           linecolor='white',
                           linewidth=2,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=10,
                               color='white'
                           )
                           ),

                yaxis=dict(title='Current Stock',
                           color='white',
                           showline=True,
                           showgrid=True,
                           showticklabels=True,
                           linecolor='white',
                           linewidth=2,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='white'
                           )
                           ),

                # legend={
                #     'orientation': 'h',
                #     'bgcolor': '#1f2c56',
                #     'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='white'),
            )

        }

        product_wise_stock_data = {
            'data': [go.Bar(x=df_stock['ProductName'],
                            y=df_stock['CurrentStock'],
                            name='',
                            marker=dict(color='orange'),
                            # hoverinfo='text',
                            # hovertext=str(stock_df['CurrentStock'])
                            ),
                     # go.Scatter(x=category_grouped_df['ProductCategoryName'],
                     #            y=category_grouped_df['CurrentStock'],
                     #            mode='lines',
                     #            name='',
                     #            line=dict(width=3, color='#FF00FF'),
                     #            marker=dict(
                     #                color='green'),
                     #            hoverinfo='text',
                     #            hovertext=''
                     #            )
                     ],

            'layout': go.Layout(
                plot_bgcolor='#1f2c56',
                paper_bgcolor='#1f2c56',
                title={
                    'text': 'Product',
                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'white',
                    'size': 20},

                hovermode='x',
                margin=dict(r=0),
                xaxis=dict(title='',
                           color='white',
                           showline=True,
                           showgrid=True,
                           showticklabels=True,
                           linecolor='white',
                           linewidth=2,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=6,
                               color='white'
                           )
                           ),

                yaxis=dict(title='Current Stock',
                           color='white',
                           showline=True,
                           showgrid=True,
                           showticklabels=True,
                           linecolor='white',
                           linewidth=2,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='white'
                           )
                           ),
                legend={
                    'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='white'),
            )

        }

        # df_category_stock = category_grouped_df[["ProductCategoryName", "CurrentStock"]]
        # df_category_stock.rename(columns={'ProductCategoryName': 'Category', 'CurrentStock': 'Stock'}, inplace=True)
        # df_product_stock = df_stock[["ProductName", "CurrentStock"]]
        # df_product_stock.rename(columns={'ProductName': 'Product', 'CurrentStock': 'Stock'}, inplace=True)

        return category_wise_stock_data, product_wise_stock_data, \
               # [{"name": i, "id": i} for i in df_category_stock.columns], df_category_stock.to_dict('records'),\
               # [{"name": i, "id": i} for i in df_product_stock.columns], df_product_stock.to_dict('records')
