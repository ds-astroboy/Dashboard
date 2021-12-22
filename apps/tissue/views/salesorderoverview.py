
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app
from common.dateinfo import *

from service_layer.services import get_service_secondary_sales_data, get_service_division_dropdown

division_values = get_service_division_dropdown()
default_value = division_values[1]['value']

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Secondary Sales', style={'fontSize': 30}),
            ], className='text-white', style={'text-align': 'center'})
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    dbc.Row([
                        dbc.Col([], md=3),
                        dbc.Col([
                            dbc.Label('Division: ', color="white"),
                            dcc.Dropdown(
                                id='division_sales_dropdown',
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
                        dcc.Graph(id='bargraph_party', figure={})
                        ], className="create_container")
                    ]),
                ], className="text-white"),
        ], md=3, style={'text-align': 'center'}),

        dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                        dcc.Graph(id='bargraph_executive', figure={})
                        ], className="create_container")
                    ]),
                ], className="text-white"),
        ], md=3, style={'text-align': 'center'}),
        dbc.Col([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='bargraph_sales', figure={})
                    ], className="create_container")
                ]),
            ], className="text-white"),
        ], md=6, style={'text-align': 'center'}),
    ]),
    # dbc.Row([
    #            # https://hexcolor.co/hex/1f2c56    Color picker
    #             dbc.Col([
    #               html.Div([
    #                 html.Div([
    #                     html.H4('Party info', style={'color': 'white'}),
    #                   ], style={'text-align': 'left'}),
    #                 dash_table.DataTable(id='datatable_party',
    #                                      data=[],
    #                                      fixed_rows={'headers': True},
    #                                      style_table={'height': 400},
    #                                      style_header={
    #                                             'backgroundColor': '#1f2c56',
    #                                              'color': 'white',
    #                                               'fontWeight': 'bold'
    #                                                 },
    #                                      style_data_conditional=[{
    #                                          'if': {'column_editable': False},
    #                                          'backgroundColor': '#1f2c56',
    #                                          'color': 'white'
    #                                      }],
    #                                      )
    #             ], className="create_container"),
    #             ], md=3, style={'text-align': 'center'}),
    #
    #             dbc.Col([
    #               html.Div([
    #                 html.Div([
    #                     html.H4('Executive info', style={'color': 'white'}),
    #                   ], style={'text-align': 'left'}),
    #                 dash_table.DataTable(id='datatable_executive',
    #                                      data=[],
    #                                      fixed_rows={'headers': True},
    #                                      style_table={'height': 400},
    #                                      style_header={
    #                                             'backgroundColor': '#1f2c56',
    #                                              'color': 'white',
    #                                               'fontWeight': 'bold'
    #                                                 },
    #                                      style_data_conditional=[{
    #                                          'if': {'column_editable': False},
    #                                          'backgroundColor': '#1f2c56',
    #                                          'color': 'white'
    #                                      }],
    #                                      )
    #             ], className="create_container"),
    #             ], md=3, style={'text-align': 'center'}),
    #       dbc.Col([
    #          html.Div([
    #              html.Div([
    #                  html.H4('Day wise sales info', style={'color': 'white'}),
    #              ], style={'text-align': 'left'}),
    #              dash_table.DataTable(id='datatable_sales',
    #                                   data=[],
    #                                   fixed_rows={'headers': True},
    #                                   style_table={'height': 400},
    #                                   style_header={
    #                                       'backgroundColor': '#1f2c56',
    #                                       'color': 'white',
    #                                       'fontWeight': 'bold'
    #                                   },
    #                                   style_data_conditional=[{
    #                                       'if': {'column_editable': False},
    #                                       'backgroundColor': '#1f2c56',
    #                                       'color': 'white'
    #                                   }],
    #                                   )
    #          ], className="create_container"),
    #         ], md=6, style={'text-align': 'center'}),
    #         ])

])

@app.callback(

    Output('bargraph_party', 'figure'),
    Output('bargraph_executive', 'figure'),
    Output('bargraph_sales', 'figure'),
    # Output('datatable_party', 'columns'),
    # Output('datatable_party', 'data'),
    # Output('datatable_executive', 'columns'),
    # Output('datatable_executive', 'data'),
    # Output('datatable_sales', 'columns'),
    # Output('datatable_sales', 'data'),

    Input('division_sales_dropdown', 'value'),
    Input('start_date', 'date'),
    Input('end_date', 'date'),
)
def update_salesorder_dashboard(division_dropdown_value, start_date, end_date):

    df = get_service_secondary_sales_data(division_dropdown_value, start_date, end_date)
    if not df.empty:
        df_party = df.groupby(["PartyName"], as_index=False)["TotalOrderPrice"].sum().sort_values("TotalOrderPrice", ascending=False)
        df_ten_top_party = df_party.head(10)
        figure_party = {
            'data': [go.Bar(x=df_ten_top_party['PartyName'],
                            y=df_ten_top_party['TotalOrderPrice'],
                            marker=dict(color='#37C2FA'),
                            # hoverinfo='text',
                            # hovertext=''
                            ),
                     ],

            'layout': go.Layout(
                plot_bgcolor='#1f2c56',
                paper_bgcolor='#1f2c56',
                title={
                    'text': 'Top 10 Party',
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
                               size=12,
                               color='white'
                           )
                           ),

                yaxis=dict(title='Total Sales',
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
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='white'),
            )

        }

        df_executive = df.groupby(["ExecutiveName"], as_index=False)["TotalOrderPrice"].sum().sort_values("TotalOrderPrice", ascending=False)
        df_top_ten_executive = df_executive.head(10)

        figure_executive = {
            'data': [go.Bar(x=df_top_ten_executive['ExecutiveName'],
                            y=df_top_ten_executive['TotalOrderPrice'],
                            marker=dict(color='#32b25f'),
                            # hoverinfo='text',
                            # hovertext=''
                            ),
                     ],

            'layout': go.Layout(
                plot_bgcolor='#1f2c56',
                paper_bgcolor='#1f2c56',
                title={
                    'text': 'Top 10 Executive',
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
                               size=12,
                               color='white'
                           )

                           ),

                yaxis=dict(title='Total Sales',
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
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='white'),
            )

        }
        df_sales = df.groupby(["OrderDate"], as_index=False)["TotalOrderPrice"].sum()
        figure_sales = {
            'data': [go.Bar(x=df_sales['OrderDate'],
                            y=df_sales['TotalOrderPrice'],
                            marker=dict(color='orange'),
                            # hoverinfo='text',
                            # hovertext=''

                            ),
                     go.Scatter(x=df_sales['OrderDate'],
                                y=df_sales['TotalOrderPrice'],
                                mode='lines',
                                name='',
                                line=dict(width=3, color='#FF00FF'),
                                marker=dict(
                                    color='green'),
                                hoverinfo='text',
                                hovertext=''
                                )
                     ],

            'layout': go.Layout(
                plot_bgcolor='#1f2c56',
                paper_bgcolor='#1f2c56',
                title={
                    'text': 'Day wise sales',
                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'white',
                    'size': 20},

                hovermode='x',
                margin=dict(r=0),
                xaxis=dict(title='Day',
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

                yaxis=dict(title='Total Sales',
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
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='white'),
            )

        }
        # df_party_data = df_party[["PartyName", "TotalOrderPrice"]]
        # df_party_data.rename(columns={'PartyName': 'Party', 'TotalOrderPrice': 'Total Sales'}, inplace=True)
        # df_executive_data = df_executive[["ExecutiveName", "TotalOrderPrice"]]
        # df_executive_data.rename(columns={'ExecutiveName': 'Executive', 'TotalOrderPrice': 'Total Sales'}, inplace=True)
        # df_sales_date = df_sales[["OrderDate", "TotalOrderPrice"]]
        # df_sales_date.rename(columns={'OrderDate': 'Order Date', 'TotalOrderPrice': 'Total Sales'}, inplace=True)

        return figure_party, figure_executive, figure_sales,\
               # [{"name": i, "id": i} for i in df_party_data.columns], df_party_data.to_dict('records'),\
               # [{"name": i, "id": i} for i in df_executive_data.columns], df_executive_data.to_dict('records'),\
               # [{"name": i, "id": i} for i in df_sales_date.columns], df_sales_date.to_dict('records')