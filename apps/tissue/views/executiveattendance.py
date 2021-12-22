
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.graph_objs as go

from app import app

from service_layer.services import get_service_division_dropdown, get_service_division_wise_area_dropdown,\
    get_service_all_division_executive_count_data, get_service_all_division_attendance_data, get_service_attendance_data, get_service_executive_count_data
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
                html.H4('Attendance', style={'fontSize': 30}),
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
                                id='division_attendance_dropdown',
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
    ], style={'display': 'none'}),

    dbc.Row(id="Div1")

])


def get_figure_content(df_executive, df_attendance, MC_Id, market_channel):

    executive_MC = df_executive[df_executive["MC_Id"] == MC_Id]
    executive_count = executive_MC["Executive_Id"].count()
    present_count = df_attendance.query(f'MC_Id == {MC_Id} & Status == "Present"')['Executive'].nunique()
    leave_count = df_attendance.query(f'MC_Id == {MC_Id} & Status == "Absent"')['Executive'].nunique()
    absent_count = executive_count - (present_count + leave_count)
    attendance_colors = ['#32b25f', '#37C2FA', '#F2DB44', '#FC3848']
    labels = ['Executive', 'Present', 'Leave', 'Absent']
    attendance_pie = {
        'data': [go.Pie(labels=labels,
                        values=[executive_count, present_count, leave_count, absent_count],
                        marker=dict(colors=attendance_colors),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        hole=.5,
                        rotation=45
                        )],

        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': market_channel,
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 25},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="sans-serif",
                size=15,
                color='white')
        ),
    }

    return attendance_pie

@app.callback(
    Output('Div1', 'children'),
    Input('division_attendance_dropdown', 'value'),
    Input('start_date', 'date'),
    Input('end_date', 'date'),
)

def update_attendance(division_dropdown_value, start_date, end_date):

    start_date = '10/13/2021'
    end_date = start_date
    content = []
    df_executive = get_service_all_division_executive_count_data()
    df_attendance = get_service_all_division_attendance_data(start_date, end_date)
    df_MC = df_executive.groupby(['MC_Id', 'MarketChannel'])['MC_Id'].nunique()
    for item in df_MC.iteritems():
        figure = get_figure_content(df_executive, df_attendance, item[0][0], item[0][1])
        content.append(
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(id='bar_attendance_' + str(item[0][1]), figure=figure),
                        ], className="create_container")
                    ]),
                ], className="text-white"),
            ], md=3),
        )
    return content

