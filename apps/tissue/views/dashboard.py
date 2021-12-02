
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from app import app
from configuration.dropdown_mgt import get_divisions, division_wise_areas, area_wise_territory, get_all_divisions
# from apps.tissue.model.models import get_all_division_attendance_dash_data
from service_layer.services import get_service_marketchannel_stock, get_service_executive_count_data, get_service_all_division_attendance_data, get_service_secondary_sales_data
from common.dateinfo import *

# https://dash.plotly.com/dash-core-components/graph
# https://pbpython.com/plotly-dash-intro.html
# https://bootswatch.com/flatly/
# https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/ch04.html

# division_values = get_service_division_dropdown()
# default_value = 0
# for item in division_values[1].items():
#     default_value = item[1]

layout = html.Div([

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('BPML Monitoring Dashboard', style={'fontSize': 30}),
               ], className='text-white', style={'text-align': 'center'})
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.Div([
                    dcc.DatePickerSingle(
                        id='start_date',
                        date=start_day_of_prev_month
                    )
                ], style={'display': 'none'}),
            ])
        ]),
    ]),

    dbc.Row([
        dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                                dbc.Row([
                                    dbc.Col([
                                    html.Div([
                                        html.H4('ATTENDANCE', className="container_top_text_color"),
                                    ])
                                    ]),
                                    dbc.Col([
                                     html.Div([
                                        dcc.Link('DETAILS', href='/executiveattendance', target="_blank", className="btn btn-primary btn-lg"),
                                    ], style={'text-align': 'left'})
                                    ])
                                ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                            html.Div([
                                html.H6('EXECUTIVE', className="header_text_size" ),
                                html.P(id="total_executive", className="header_text_value_size"),
                                html.H6('LEAVE',className="header_text_size"),
                                html.P(id="total_leave", className="header_text_value_size"),
                                ]),
                            ]),
                            dbc.Col([
                            html.Div([
                              html.H6('PRESENT',  className="header_text_size"),
                                html.P(id="total_attendance", className="header_text_value_size" ),
                                html.H6('ABSENT',  className="header_text_size" ),
                                html.P(id="total_absent", className="header_text_value_size")
                              ]),
                            ]),
                        ])
                        ], className="create_container"),
                        html.Div([
                        dcc.Graph(id='attendance_executive_pie', figure={})
                        ], className="create_container")
                    ]),
                ], className="text-white"),
        ], md=4, style={'text-align': 'center'}),

        dbc.Col([
                html.Div([
                    html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H4('SALES', className="container_top_text_color"),
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    dcc.Link('DETAILS', href='/salesorderoverview', target="_blank",
                                             className="btn btn-primary btn-lg"),
                                ], style={'text-align': 'left'})
                            ])
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                            html.Div([
                                html.H6('TOTAL ORDER', className="header_text_size"),
                                html.P(id="total_order",   className="header_text_value_size"),
                                html.H6('SALES AMOUNT', className="header_text_size"),
                                html.P(id="total_sales_amount",  className="header_text_value_size"),
                                  ]),
                            ]),
                            dbc.Col([
                            html.Div([
                            html.H6('ORDER QUANTITY', className="header_text_size"),
                            html.P(id="total_order_qty",  className="header_text_value_size" ),
                                html.H6('REMAINING', className="header_text_size"),
                                html.P(id="total_remain_qty",  className="header_text_value_size")
                              ]),
                            ]),
                        ]),
                        ], className="create_container"),
                        html.Div([
                        dcc.Graph(id='sales_order_pie', figure={})
                        ], className="create_container")
                    ]),
                ], className="text-white"),
        ], md=4, style={'text-align': 'center'}),

        dbc.Col([
            html.Div([
                html.Div([
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.H4('STOCK', className="container_top_text_color"),
                                    ])
                                ]),
                                dbc.Col([
                                    html.Div([
                                        dcc.Link('DETAILS', href='/productstocksummary', target="_blank", className="btn btn-primary btn-lg"),
                                    ], style={'text-align': 'left'})
                                ])
                            ]),
                        html.Br(),
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H6('DELIVERED', className="header_text_size"),
                                html.P(id="delivered_qty", className="header_text_value_size"),
                                html.H6('STOCK', className="header_text_size"),
                                html.P(id="stock_qty", className="header_text_value_size")


                            ]),
                        ]),
                        dbc.Col([
                            html.Div([
                                html.H6('RECEIVED', className="header_text_size"),
                                html.P(id="received_qty",  className="header_text_value_size"),
                                # html.H6('PENDING', className="header_text_size"),
                                # html.P(id="pending_qty",  className="header_text_value_size"),
                            ]),
                        ]),
                    ]),
                    ], className="create_container"),
                    html.Div([
                        dcc.Graph(id='stock_pie', figure={})
                    ], className="create_container")
                ]),
            ], className="text-white"),
        ], md=4, style={'text-align': 'center'}),

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

    # Output('order_qty', 'children'),
    # Output('sa_order', 'children'),
    Output('received_qty', 'children'),
    Output('delivered_qty', 'children'),
    Output('stock_qty', 'children'),
    # Output('pending_qty', 'children'),

    Input('start_date', 'date'),

    # Input('end_date', 'date'),
)

def update_dashboard(start_date):
    start_date = '10/13/2021'
    end_date = start_date
    df_executive_count = get_service_executive_count_data(0)
    df_attendance = get_service_all_division_attendance_data(start_date, end_date)
    executive_count = df_executive_count["Executive_Id"].count()
    present_count = df_attendance[df_attendance['Status'] == 'Present']['Executive'].nunique()
    leave_count = df_attendance[df_attendance['Status'] == 'Leave']['Executive'].nunique()
    absent_count = executive_count - (present_count + leave_count)

    pie_data = []
    attendance_colors = ['#3966FA', '#76D695', '#F2DB44', '#DB4216']
    pie_data.append({'Status': 'Executive', 'Count': executive_count})
    pie_data.append({'Status': 'Present', 'Count': present_count})
    pie_data.append({'Status': 'Leave', 'Count': leave_count})
    pie_data.append({'Status': 'Absent', 'Count': absent_count})
    df_bar = pd.DataFrame(pie_data)
    # attendance_pie = px.bar(df_bar, x="Status", y="Count", color=df_bar['color'])

    attendance_bar = {
        'data': [go.Bar(x=df_bar['Status'],
                        y=df_bar['Count'],
                        name='',
                        marker=dict(color=attendance_colors),
                        hoverinfo='text',
                        hovertext='Executive ' + str(executive_count) + ' Present ' + str(present_count) + ' Leave ' + str(leave_count) + ' Absent ' + str(absent_count)

                        ),
                 go.Scatter(x=df_bar['Status'],
                            y=df_bar['Count'],
                            mode='lines',
                            name='',
                            line=dict(width=3, color='#FF00FF'),
                            marker=dict(
                                color='green'),
                            hoverinfo='text',
                            hovertext='Executive ' + str(executive_count) + ' Present ' + str(present_count) + ' Leave ' + str(leave_count) + ' Absent ' + str(absent_count)
                            )
                 ],

        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            title={
                'text': 'Attendance',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 20},

            hovermode='x',
            margin=dict(r=0),
            xaxis=dict(title='Status',
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

            yaxis=dict(title='Count',
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

    df_sales_order = get_service_secondary_sales_data(None, start_date, end_date)
    order_count = df_sales_order["Code"].nunique()
    total_sales_amount = round(df_sales_order["TotalOrderPrice"].sum(), 2)
    total_order_qty = df_sales_order["TotalOrderQty"].sum()
    total_remaining_qty = df_sales_order["RemainingQty"].sum()
    labels = ["Total Order Qty", "Remaining Qty"]
    sales_color = ["#75D692", 'orange']
    sales_order_pie = {
        'data': [go.Pie(labels=labels,
                        values=[total_order_qty, total_remaining_qty],
                        marker=dict(colors=sales_color),
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
                'text': 'Sales',
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
    stock_df = get_service_marketchannel_stock(0, start_date, end_date)
    received_qty = stock_df['ReceivedQty'].sum()
    delivered_qty = stock_df['DeliveredQty'].sum()
    stock_qty = stock_df['Stock'].sum()
    # pending_qty = 250000
    stock_colors = ['#60E0BF', '#95F777', 'green']
    stock_pie = {
        'data': [go.Pie(labels=['Received', 'Delivered', 'Stock'],
                        values=[received_qty, delivered_qty, stock_qty],
                        marker=dict(colors=stock_colors),
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
                'text': 'Stock',
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
    return attendance_bar, sales_order_pie, stock_pie, executive_count, present_count, leave_count, absent_count, order_count, total_sales_amount, total_order_qty, total_remaining_qty, \
         received_qty, delivered_qty, stock_qty












# @app.callback(
#     Output('attendance_executive_pie', 'figure'),
#
#     Output('total_executive', 'children'),
#     Output('total_attendance', 'children'),
#     Output('total_leave', 'children'),
#     Output('total_absent', 'children'),
#     Input('start_date', 'date'),
#     # Input('end_date', 'date'),
# )
# def update_dashboard(start_date):
#     start_date = '10/13/2021'
#     end_date = start_date
#     df_executive_count = get_executive_count_dash_data(0)
#     df_attendance = get_all_division_attendance_dash_data(start_date, end_date)
#     executive_count = df_executive_count["Executive_Id"].count()
#     present_count = df_attendance[df_attendance['Status'] == 'Present']['Executive'].nunique()
#     leave_count = df_attendance[df_attendance['Status'] == 'Leave']['Executive'].nunique()
#     absent_count = executive_count - (present_count + leave_count)
#
#     pie_data = []
#     attendance_colors = ['#3966FA', '#76D695', '#F2DB44', '#DB4216']
#     pie_data.append({'Status': 'Executive', 'Count': executive_count})
#     pie_data.append({'Status': 'Present', 'Count': present_count})
#     pie_data.append({'Status': 'Leave', 'Count': leave_count})
#     pie_data.append({'Status': 'Absent', 'Count': absent_count})
#     df_bar = pd.DataFrame(pie_data)
#
#     attendance_bar = {
#         'data': [go.Bar(x=df_bar['Status'],
#                         y=df_bar['Count'],
#                         name='',
#                         marker=dict(color=attendance_colors),
#                         hoverinfo='text',
#                         hovertext='Executive ' + str(executive_count) + ' Present ' + str(present_count) + ' Leave ' + str(leave_count) + ' Absent ' + str(absent_count)
#
#                         ),
#                  go.Scatter(x=df_bar['Status'],
#                             y=df_bar['Count'],
#                             mode='lines',
#                             name='',
#                             line=dict(width=3, color='#FF00FF'),
#                             marker=dict(
#                                 color='green'),
#                             hoverinfo='text',
#                             hovertext='Executive ' + str(executive_count) + ' Present ' + str(present_count) + ' Leave ' + str(leave_count) + ' Absent ' + str(absent_count)
#                             )
#                  ],
#
#         'layout': go.Layout(
#             plot_bgcolor='#1f2c56',
#             paper_bgcolor='#1f2c56',
#             title={
#                 'text': 'Attendance',
#                 'y': 0.93,
#                 'x': 0.5,
#                 'xanchor': 'center',
#                 'yanchor': 'top'},
#             titlefont={
#                 'color': 'white',
#                 'size': 20},
#
#             hovermode='x',
#             margin=dict(r=0),
#             xaxis=dict(title='Status',
#                        color='white',
#                        showline=True,
#                        showgrid=True,
#                        showticklabels=True,
#                        linecolor='white',
#                        linewidth=2,
#                        ticks='outside',
#                        tickfont=dict(
#                            family='Arial',
#                            size=12,
#                            color='white'
#                        )
#
#                        ),
#
#             yaxis=dict(title='Count',
#                        color='white',
#                        showline=True,
#                        showgrid=True,
#                        showticklabels=True,
#                        linecolor='white',
#                        linewidth=2,
#                        ticks='outside',
#                        tickfont=dict(
#                            family='Arial',
#                            size=12,
#                            color='white'
#                        )
#
#                        ),
#
#             # legend={
#             #     'orientation': 'h',
#             #     'bgcolor': '#1f2c56',
#             #     'xanchor': 'center', 'x': 0.5, 'y': -0.3},
#             font=dict(
#                 family="sans-serif",
#                 size=12,
#                 color='white'),
#         )
#
#     }
#     return attendance_bar, executive_count, present_count, leave_count, absent_count
#
# @app.callback(
#     Output('sales_order_pie', 'figure'),
#
#     Output('total_order', 'children'),
#     Output('total_sales_amount', 'children'),
#     Output('total_order_qty', 'children'),
#     Output('total_remain_qty', 'children'),
#
#     Input('start_date', 'date'),
#     # Input('end_date', 'date'),
# )
# def update_dashboard(start_date):
#     start_date = '10/13/2021'
#     end_date = start_date
#     df_sales_order = get_sales_Dash_data(None, start_date, end_date)
#     order_count = df_sales_order["Code"].nunique()
#     total_sales_amount = df_sales_order["TotalOrderPrice"].sum()
#     total_order_qty = df_sales_order["TotalOrderQty"].sum()
#     total_remaining_qty = df_sales_order["RemainingQty"].sum()
#     labels = ["Total Order Qty", "Remaining Qty"]
#     sales_color = ["#75D692", 'orange']
#     sales_order_pie = {
#         'data': [go.Pie(labels=labels,
#                         values=[total_order_qty, total_remaining_qty],
#                         marker=dict(colors=sales_color),
#                         hoverinfo='label+value+percent',
#                         textinfo='label+value',
#                         textfont=dict(size=13),
#                         hole=.5,
#                         rotation=45
#                         )],
#
#         'layout': go.Layout(
#             plot_bgcolor='#1f2c56',
#             paper_bgcolor='#1f2c56',
#             hovermode='closest',
#             title={
#                 'text': 'Sales',
#                 'y': 0.93,
#                 'x': 0.5,
#                 'xanchor': 'center',
#                 'yanchor': 'top'},
#             titlefont={
#                 'color': 'white',
#                 'size': 25},
#             legend={
#                 'orientation': 'h',
#                 'bgcolor': '#1f2c56',
#                 'xanchor': 'center', 'x': 0.5, 'y': -0.07},
#             font=dict(
#                 family="sans-serif",
#                 size=15,
#                 color='white')
#         ),
#     }
#     return sales_order_pie, order_count, total_sales_amount, total_order_qty, total_remaining_qty
#
# @app.callback(
#
#     Output('stock_pie', 'figure'),
#
#     Output('received_qty', 'children'),
#     Output('delivered_qty', 'children'),
#     Output('stock_qty', 'children'),
#
#     Input('start_date', 'date'),
#     # Input('end_date', 'date'),
# )
# def update_dashboard(start_date):
#     start_date = '10/13/2021'
#     end_date = start_date
#     stock_df = get_marketchannel_stock(0, start_date, end_date)
#     received_qty = stock_df['ReceivedQty'].sum()
#     delivered_qty = stock_df['DeliveredQty'].sum()
#     stock_qty = stock_df['Stock'].sum()
#     # pending_qty = 250000
#     stock_colors = ['yellow', '#15D63B', '#FF4848', '#4BF7A8']
#     stock_pie = {
#         'data': [go.Pie(labels=['Received', 'Delivered', 'Stock'],
#                         values=[received_qty, delivered_qty, stock_qty],
#                         marker=dict(colors=stock_colors),
#                         hoverinfo='label+value+percent',
#                         textinfo='label+value',
#                         textfont=dict(size=13),
#                         hole=.5,
#                         rotation=45
#                         )],
#
#         'layout': go.Layout(
#             plot_bgcolor='#1f2c56',
#             paper_bgcolor='#1f2c56',
#             hovermode='closest',
#             title={
#                 'text': 'Stock',
#                 'y': 0.93,
#                 'x': 0.5,
#                 'xanchor': 'center',
#                 'yanchor': 'top'},
#             titlefont={
#                 'color': 'white',
#                 'size': 25},
#             legend={
#                 'orientation': 'h',
#                 'bgcolor': '#1f2c56',
#                 'xanchor': 'center', 'x': 0.5, 'y': -0.07},
#             font=dict(
#                 family="sans-serif",
#                 size=15,
#                 color='white')
#         ),
#
#     }
#     return stock_pie, received_qty, delivered_qty, stock_qty


