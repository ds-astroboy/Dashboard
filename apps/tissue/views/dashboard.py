
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

# https://dash.plotly.com/dash-core-components/graph
# https://pbpython.com/plotly-dash-intro.html
# https://bootswatch.com/flatly/
# https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/ch04.html

division_values = get_divisions()
default_value = 0
# for item in division_values[1].items():
#     default_value = item[1]

layout = html.Div([
     #
     # html.Div([
     #     html.H4("This is  a test")
     # ],  style={'text-align': 'center'}),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('BPML Monitoring Dashboard', style={'fontSize': 30}),
               ], className='text-white', style={'text-align': 'center'})
        ], md=12),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                # dbc.Col([], md=4),
                html.Div([
                    # html.H6('Attendance Date'),
                    dcc.DatePickerSingle(
                        id='start_date',
                        date=start_day_of_prev_month
                    )
                ], style={'display': 'none'}),
             # dbc.Col([], md=4),
            ], )
        ], md=12),
    ]),

    dbc.Row([
        # dbc.Col([], md=1),
        dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                        html.H4('Attendance', className="container_top_text_color"),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                            html.Div([
                                html.H6('Total Executive',
                                        style={
                                            'text-align': 'left',
                                            'font-weight': 300,
                                            'fontSize': 18},
                                        ),
                                html.P(id="total_executive",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       ),

                                html.H6('Leave',
                                        style={
                                            'text-align': 'left',
                                            'font-weight': 'bold',
                                            'fontSize': 18}
                                        ),
                                html.P(id="total_leave",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       ),
                                  ]),
                            ]),
                            dbc.Col([
                            html.Div([
                              html.H6('Attendance',
                                        style={
                                            'text-align': 'left',
                                            'font-weight': 'bold',
                                            'fontSize': 18}
                                        ),
                                html.P(id="total_attendance",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       ),
                                html.H6('Absent',
                                        style={
                                            'text-align': 'left',
                                            'font-weight': 'bold',
                                            'fontSize': 18}
                                        ),
                                html.P(id="total_absent",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       )
                              ]),
                            ]),
                        ])
                        ], className="create_container"),
                        html.Div([
                        dcc.Graph(id='attendance_executive_pie', figure={})
                        ], className="create_container")
                    ], className=""),
                ], className="text-white"),
        ], md=3, style={'text-align': 'center'}),

        dbc.Col([
                html.Div([
                    html.Div([
                    html.Div([
                        html.H4('Sales', className="container_top_text_color"),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                            html.Div([
                                html.H6('Total Order',
                                        style={
                                            'text-align': 'left',
                                            'font-weight': 'bold',
                                            'fontSize': 18}
                                        ),
                                html.P(id="total_order",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       ),
                                html.H6('Sales Amount',
                                        style={
                                            'text-align': 'left',
                                            'font-weight': 'bold',
                                            'fontSize': 18}
                                        ),
                                html.P(id="total_sales_amount",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       ),
                                  ]),
                            ]),
                            dbc.Col([
                            html.Div([
                            html.H6('Order Quantity',
                                    style={
                                        'text-align': 'left',
                                        'font-weight': 'bold',
                                        'fontSize': 18}
                                    ),
                            html.P(id="total_order_qty",
                                   style={
                                       'text-align': 'left',
                                       'color': 'orange',
                                       'fontSize': 25}
                                   ),
                                html.H6('Remaining Quantity',
                                        style={
                                            'text-align': 'left',
                                            'font-weight': 'bold',
                                            'fontSize': 18}
                                        ),
                                html.P(id="total_remain_qty",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       )
                              ]),
                            ]),
                        ]),
                        ], className="create_container"),
                        html.Div([
                        dcc.Graph(id='sales_order_pie', figure={})
                        ], className="create_container")
                    ], className=""),
                ], className="text-white"),
        ], md=4, style={'text-align': 'center'}),

        dbc.Col([
            html.Div([
                html.Div([

                        html.Div([
                        html.H4('Stock', className="container_top_text_color"),
                        html.Br(),
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H6('Order Quantity',
                                        style={
                                            'text-align': 'left',
                                            'font-weight': 'bold',
                                            'fontSize': 18}
                                        ),
                                html.P(id="order_qty",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       ),

                                html.H6('Delivered',
                                        style={
                                            'text-align': 'left',
                                            'font-weight': 'bold',
                                            'fontSize': 18}
                                        ),
                                html.P(id="delivered_qty",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       ),
                            ]),
                        ]),
                        dbc.Col([
                            html.Div([
                                html.H6('SA Order',
                                        style={
                                            'text-align': 'left',
                                            'font-weight': 'bold',
                                            'fontSize': 18}
                                        ),
                                html.P(id="sa_order",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       ),
                                html.H6('Pending',
                                        style={
                                            'textAlign': 'left',
                                            'font-weight': 'bold',
                                            'fontSize': 18}
                                        ),
                                html.P(id="pending_qty",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       ),
                            ]),
                        ]),
                        dbc.Col([
                            html.Div([
                                html.H6('Received',
                                        style={
                                            'text-align': 'left',
                                            'fontSize': 18}
                                        ),
                                html.P(id="received_qty",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       ),
                                     html.H6('Stock',
                                        style={
                                            'text-align': 'left',
                                            'fontSize': 18}
                                        ),
                                     html.P(id="stock_qty",
                                       style={
                                           'text-align': 'left',
                                           'color': 'orange',
                                           'fontSize': 25}
                                       )
                            ]),
                        ]),
                    ]),
                    ], className="create_container"),
                    html.Div([
                        dcc.Graph(id='stock_pie', figure={})
                    ], className="create_container")
                ], className=""),
            ], className="text-white"),
        ], md=5, style={'text-align': 'center'}),

    # dbc.Col([], md=1),
    ]),

])


@app.callback(
    Output('attendance_executive_pie', 'figure'),
    Output('sales_order_pie', 'figure'),
    Output('stock_pie', 'figure'),

    Output('total_executive', 'children'),
    Output('total_attendance', 'children'),
    Output('total_leave', 'children'),
    Output('total_absent', 'children'),

    Output('total_order', 'children'),
    Output('total_sales_amount', 'children'),
    Output('total_order_qty', 'children'),
    Output('total_remain_qty', 'children'),

    Output('order_qty', 'children'),
    Output('sa_order', 'children'),
    Output('received_qty', 'children'),
    Output('delivered_qty', 'children'),
    Output('stock_qty', 'children'),
    Output('pending_qty', 'children'),

    Input('start_date', 'date'),

    # Input('end_date', 'date'),
)

def update_dashboard(start_date):
    start_date = '10/13/2021'
    end_date = start_date
    # attendance_pie = {}
    # sales_order_pie = {}
    # total_exeutive = []
    # sales_table_data = []
    df_executive_count = get_executive_count_dash_data(0)
    df_attendance = get_all_division_attendance_dash_data(start_date, end_date)
    executive_count = df_executive_count["Executive_Id"].count()
    present_count = df_attendance[df_attendance['Status'] == 'Present']['Executive'].nunique()
    leave_count = df_attendance[df_attendance['Status'] == 'Leave']['Executive'].nunique()
    absent_count = executive_count - (present_count + leave_count)

    # total_exeutive.append({"Total Executive": executive_count,
    #                                  "Present Executive": present_count,
    #                                  "Leave Executive": leave_count,
    #                                  "Absent Executive": absent_count,
    #                                  })
    # executive_table = pd.DataFrame(total_exeutive)

    # pie_data = []
    # colors = ['green', 'orange', 'red']
    # pie_data.append({'Status': 'Present', 'Count': present_count, 'color': "green"})
    # pie_data.append({'Status': 'Leave', 'Count': leave_count, 'color': "yellow"})
    # pie_data.append({'Status': 'Absent', 'Count': absent_count, 'color': "red"})
    # df_bar = pd.DataFrame(pie_data)
    # attendance_pie = px.bar(df_bar, x="Status", y="Count", color=df_bar['color'])

    colors = ['#4BF7A8', 'orange', 'red']
    # labels = ["Present", "Leave", "Absent"]
    # attendance_pie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    # attendance_pie.add_trace(go.Pie(labels=labels, values=[present_count, leave_count, absent_count],  marker=dict(colors=colors)), 1, 1)
    # attendance_pie.update_traces(hole=.6, hoverinfo="label+percent")
    #
    # attendance_pie.update_layout(
    #     legend=dict(
    #     orientation="h",
    #     yanchor="bottom",
    #     y=1.02,
    #     xanchor="right",
    #     x=1
    # ),
    # margin=dict(l=80, r=20, t=80, b=20),
    # )

    attendance_pie = {
        'data': [go.Pie(labels=['Present', 'Leave', 'Absent'],
                        values=[present_count, leave_count, absent_count],
                        marker=dict(colors=colors),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        hole=.7,
                        rotation=45
                        )],

        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': '',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="sans-serif",
                size=12,
                color='white')
        ),
    }

    df_sales_order = get_sales_Dash_data(None, start_date, end_date)
    order_count = df_sales_order["Code"].nunique()
    total_sales_amount = df_sales_order["TotalOrderPrice"].sum()
    total_order_qty = df_sales_order["TotalOrderQty"].sum()
    total_remaining_qty = df_sales_order["RemainingQty"].sum()

    # sales_table_data.append({"Total Order": order_count,
    #                      "Total Sales Amount": '{0:.2f}'.format(total_sales_amount),
    #                      "Total Order Qty": '{0:.2f}'.format(total_order_qty),
    #                      "Total Remaining Qty": '{0:.2f}'.format(total_remaining_qty)
    #                      })
    # df_sales_table_data = pd.DataFrame(sales_table_data)

    labels = ["Total Order Qty", "Remaining Qty"]
    # sales_order_pie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    # sales_order_pie.add_trace(go.Pie(labels=labels, values=[total_order_qty, total_remaining_qty]), 1, 1)
    # sales_order_pie.update_traces(hole=.6, hoverinfo="label+percent")
    #
    # sales_order_pie.update_layout(
    #     legend=dict(
    #         orientation="h",
    #         yanchor="bottom",
    #         y=1.02,
    #         xanchor="right",
    #         x=1
    #     ),
    #     margin=dict(l=80, r=20, t=80, b=20),
    # )

    sales_order_pie = {
        'data': [go.Pie(labels=labels,
                        values=[total_order_qty, total_remaining_qty],
                        marker=dict(colors=colors),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        hole=.7,
                        rotation=45
                        )],

        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': '',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="sans-serif",
                size=12,
                color='white')
        ),
    }
    order_qty = total_order_qty
    sa_order = 4565
    received_qty = 350000
    delivered_qty = 650000
    stock_qty = 700000
    pending_qty = 250000
    stock_colors = ['#4BF7A8', 'orange', 'green', 'red', 'yellow']
    stock_pie = {
        'data': [go.Pie(labels=['Order', 'Received', 'Delivered', 'Pending', 'Stock'],
                        values=[order_qty, received_qty, delivered_qty, pending_qty, stock_qty],
                        marker=dict(colors=stock_colors),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        hole=.7,
                        rotation=45
                        )],

        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': '',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="sans-serif",
                size=12,
                color='white')
        ),

    }

    return attendance_pie, sales_order_pie, stock_pie, executive_count, present_count, leave_count, absent_count, order_count, total_sales_amount, total_order_qty, total_remaining_qty, \
           order_qty, sa_order, received_qty, delivered_qty, stock_qty, pending_qty
