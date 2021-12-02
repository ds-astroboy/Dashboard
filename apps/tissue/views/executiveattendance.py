
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.graph_objs as go

from app import app
from configuration.dropdown_mgt import get_divisions, division_wise_areas, area_wise_territory, get_all_divisions
from apps.tissue.model.models import get_attendance_dash_data, get_all_division_attendance_dash_data, get_executive_count_dash_data
from service_layer.services import get_service_division_dropdown, get_service_division_wise_area_dropdown,\
    get_service_executive_count_data, get_service_all_division_attendance_data, get_service_attendance_data
from common.dateinfo import *

# https://dash.plotly.com/dash-core-components/graph
# https://pbpython.com/plotly-dash-intro.html

division_values = get_service_division_dropdown()
default_value = 0
# for item in division_values[1].items():
#     default_value = item[1]

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Attendance Status', className='card-header bg-success'),
                html.Div([
                    dbc.Row([
                        dbc.Col([], md=1),
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
                            dbc.Label('Area: '),
                            dcc.Dropdown(
                                id='area_dropdown',
                                style={
                                    'width': '90%'
                                },
                                options=[],
                                clearable=True
                            )], md=2),

                          # dbc.Col([
                          #   dbc.Label('Territory: '),
                          #   dcc.Dropdown(
                          #       id='territory_dropdown',
                          #       style={
                          #           'width': '90%'
                          #       },
                          #       options=[],
                          #       clearable=False,
                          #   )], md=3),

                        dbc.Col([
                            dbc.Label('Attendance Date: '),
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
                        # dbc.Col([
                        #
                        # ], md=1),
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
                html.H4('Overall Attendance Status', className='card-header bg-info'),
            ], style={'text-align': 'center'}),
            html.Div([dash_table.DataTable(id='attendance_summary', data=[],)], style={'font-weight': 'bold'})
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Total Attendance by Division', className='card-header bg-info'),
                dcc.Graph(id='bargraph_attendance', figure={})], style={'text-align': 'center'})
        ], md=6),
        dbc.Col([
            html.Div([
                html.H4('Executive Present Status', className='card-header bg-info'),
                dcc.Graph(id='bargraph_present_status', figure={})], style={'text-align': 'center'})
        ], md=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Executives Status Table', className='card-header bg-info'),
            ], style={'text-align': 'left'}),
            dash_table.DataTable(id='attendance_table',
                                 data=[],
                                 fixed_rows={'headers': True},
                                 style_table={'height': 400}
                                 )
        ])
    ])
])


@app.callback(
    Output('area_dropdown', 'options'),
    # Output('territory_dropdown', 'options'),
    Output('bargraph_attendance', 'figure'),
    Output('bargraph_present_status', 'figure'),
    Output('attendance_summary', 'columns'),
    Output('attendance_summary', 'data'),
    Output('attendance_table', 'columns'),
    Output('attendance_table', 'data'),
    Input('division_dropdown', 'value'),
    Input('area_dropdown', 'value'),
    # Input('territory_dropdown', 'value'),
    Input('start_date', 'date'),
    Input('end_date', 'date'),
)

def update_attendance_graph(division_dropdown_value, area_dropdown_value, start_date, end_date):

    # end_date = start_date
    figure_attendance_pie = {}
    figure_attendance_bar = {}
    figure_attenndance_summary = {}
    exeutive_summary_data = []
    areas = []
    dropdown_value = 0
    if division_dropdown_value:
        areas = get_service_division_wise_area_dropdown(division_dropdown_value)

    # if area_dropdown_value:
    #     territory = area_wise_territory(area_dropdown_value)

    if not division_dropdown_value:
        df = get_service_all_division_attendance_data(start_date, end_date)
    else:
        if division_dropdown_value:
            dropdown_value = division_dropdown_value
        if area_dropdown_value:
            dropdown_value = area_dropdown_value
        # if territory_dropdown_value:
        #     dropdown_value = territory_dropdown_value
        df = get_service_attendance_data(dropdown_value, start_date, end_date)

    df_executive_count = get_service_executive_count_data(dropdown_value)

    if not df.empty:

        if not division_dropdown_value:
            df_executive_attendance = df.loc[(df.Status == 'Present')]
            df_all = df_executive_attendance.groupby('MarketChannel').size().reset_index(name="Present")
            figure_attendance_pie = px.pie(df_all, names='MarketChannel', values='Present', height=300)
        else:
            df_custom = df.groupby('Status').size().reset_index(name='count')
            figure_attendance_pie = px.pie(df_custom, names='Status', values='count', height=300)


        df_attendance_count = df.groupby(['Executive', 'Status']).size().reset_index(name='Days')
        figure_attendance_bar = px.bar(df_attendance_count, x="Executive", y="Days", color="Status", text="Days")

        executive_count = df_executive_count["Executive_Id"].count()
        exeutive_summary_data.append({"Total Executive": executive_count,
                                     "Present Executive": df['Executive'].nunique()
                                     })
        df_executive_table = pd.DataFrame(exeutive_summary_data)

        df.rename(columns={'Name': 'Executive Name', 'MarketChannel': 'Market Channel', 'EntryDateTime': 'Attendance Date', 'Status': 'Present Status'}, inplace=True)
        dt_datatable = df[['Executive Name', 'PFNumber', 'Market Channel', 'Attendance Date', 'Present Status']]
    return areas, figure_attendance_pie, figure_attendance_bar, \
           [{"name": i, "id": i} for i in df_executive_table.columns], \
           df_executive_table.to_dict('records'), [{"name": i, "id": i} for i in dt_datatable.columns], dt_datatable.to_dict('records')
