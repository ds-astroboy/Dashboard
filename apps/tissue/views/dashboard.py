
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import plotly.graph_objs as go

from app import app
from service_layer.services import get_service_marketchannel_stock, get_service_executive_count_data, get_service_all_division_attendance_data,\
    get_service_monthly_secondary_sales_data, get_service_date_wise_secondary_sales_data, get_service_product_wise_secondary_sales_data, \
    get_service_category_wise_secondary_sales_data
from common.dateinfo import *
from common.helpler import *

# https://dash.plotly.com/dash-core-components/graph
# https://pbpython.com/plotly-dash-intro.html
# https://bootswatch.com/flatly/
# https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/ch04.html

# https://community.plotly.com/t/hyperlink-to-markers-on-map/17858   Hyperlink to markers on map

# https://resonance-analytics.com/blog/deploying-dash-apps-on-azure  deployment
# https://www.youtube.com/watch?v=x8xjj6cR9Nc     voice to text change

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('BPML Monitoring Dashboard', style={'fontSize': 30}),
               ], className='text-white', style={'text-align': 'center'})
        ]),
    ]),
    # dbc.Row([
    #     dbc.Col([
    #
    #     ], md=4)
    # ]),
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
             html.H4("Secondary Sales", style={"text-align": "center"}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Graph(id='month_wise_sales', figure={}),
                                        html.Div([
                                            dcc.Link('MORE', href='/apps/tissue/views/salesorderoverview', target="_blank",className="btn btn-primary btn-lg"),
                                        ], style={'text-align': 'right'}),
                                    ], className="create_container")
                                ]),
                            ], className="text-white"),
                        ], md=3, style={'text-align': 'center'}),
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Graph(id='day_wise_sales', figure={}),
                                        html.Div([
                                            dcc.Link('MORE', href='/apps/tissue/views/salesorderoverview', target="_blank", className="btn btn-primary btn-lg"),
                                        ], style={'text-align': 'right'}),
                                    ], className="create_container")
                                ]),
                            ], className="text-white"),
                        ], md=3, style={'text-align': 'center'}),
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Graph(id='category_wise_sales', figure={}),
                                        html.Div([
                                            dcc.Link('MORE', href='/apps/tissue/views/salesorderoverview', target="_blank",  className="btn btn-primary btn-lg"),
                                        ], style={'text-align': 'right'}),
                                    ], className="create_container")
                                ]),
                            ], className="text-white"),
                        ], md=3, style={'text-align': 'center'}),

                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Graph(id='product_wise_sales', figure={}),
                                        html.Div([
                                            dcc.Link('MORE', href='/apps/tissue/views/salesorderoverview', target="_blank", className="btn btn-primary btn-lg"),
                                        ], style={'text-align': 'right'}),
                                    ], className="create_container")
                                ]),
                            ], className="text-white"),
                        ], md=3, style={'text-align': 'center'}),

                    ]),
                ], className="card-body")
            ], className="card-header")
        ], className="card text-white bg-primary")
       ])
   ]),


    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='attendance_executive', figure={}),
                        html.Div([
                            dcc.Link('MORE', href='/apps/tissue/views/executiveattendance', target="_blank", className="btn btn-primary btn-lg"),
                        ], style={'text-align': 'right'}),
                    ], className="create_container")
                ]),
            ], className="text-white"),
        ], md=6, style={'text-align': 'center'}),

        dbc.Col([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='stock', figure={}),
                        html.Div([
                            dcc.Link('MORE', href='/apps/tissue/views/productstocksummary', target="_blank", className="btn btn-primary btn-lg"),
                        ], style={'text-align': 'right'}),
                    ], className="create_container")
                ]),
            ], className="text-white"),
        ], md=6, style={'text-align': 'center'}),

    ])

])

@app.callback(

    Output('month_wise_sales', 'figure'),
    Output('day_wise_sales', 'figure'),
    Output('product_wise_sales', 'figure'),
    Output('category_wise_sales', 'figure'),
    Output('attendance_executive', 'figure'),
    Output('stock', 'figure'),

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
    attendance_colors = ['#3966FA', '#76D695', '#F2DB44', '#FC3848']

    attendance_data = {
        'data': [go.Pie(labels=['Executive', 'Present', 'Leave', 'Absent'],
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
                'text': 'Attendance',
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

    df_secondary_sales = get_service_monthly_secondary_sales_data()
    df_secondary_sales["month"] = df_secondary_sales["Months"].apply(transform_month)
    df_secondary_sales = df_secondary_sales.sort_values(["Years", "month"])
    month_wise_sales_data = {
        'data': [go.Bar(x=df_secondary_sales['SalesAmount'],
                        y=df_secondary_sales['Month_Year'],
                        marker=dict(color='#339966'),
                        text=df_secondary_sales['SalesAmount'],
                        orientation='h'
                        ),
                 ],

        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            title={
                'text': 'Monthly Sales',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 20},

            hovermode='y',
            margin=dict(r=0),
            xaxis=dict(title='Sales',
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

            yaxis=dict(title='Month',
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
    stock_df = get_service_marketchannel_stock(0, start_date, end_date)
    received_qty = stock_df['ReceivedQty'].sum()
    delivered_qty = stock_df['DeliveredQty'].sum()
    stock_qty = stock_df['Stock'].sum()
    stock_colors = ['#60E0BF', '#95F777', 'green']
    stock_data = {
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
    df = get_service_date_wise_secondary_sales_data(0, '2021-10-01', '2021-10-10')
    df_sales = df.groupby(["OrderDate"], as_index=False)["SalesAmount"].sum()
    day_wise_sales_data = {
        'data': [go.Bar(x=df_sales['SalesAmount'],
                        y=df_sales['OrderDate'],
                        marker=dict(color='#0099cc'),
                        text=df_sales['SalesAmount'],
                        # hoverinfo='text',
                        # hovertext=''
                        orientation='h'
                        ),
                 ],
        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            title={
                'text': 'Day Wise Sales',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 20},

            hovermode='y',
            margin=dict(r=0),
            xaxis=dict(title='Sales',
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

            yaxis=dict(title='Day',
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
    df_product_wise_secondary_sales = get_service_product_wise_secondary_sales_data(0, '2021-10-01', '2021-10-31')
    df_sorted = df_product_wise_secondary_sales.sort_values('SalesAmount')
    product_wise_sales_data = {
        'data': [go.Bar(x=df_sorted['SalesAmount'],
                        y=df_sorted['ProductName'],
                        marker=dict(color='#009999'),
                        text=df_sorted['SalesAmount'],
                        # hoverinfo='text',
                        hovertext=df_sorted['ProductName'],
                        orientation='h'
                        ),
                 ],
        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            title={
                'text': 'Product Wise Sales',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 20},
            hovermode='y',
            margin=dict(r=0),
            xaxis=dict(title='Sales',
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

            yaxis=dict(title='',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=8,
                           color='white'
                       )
                       ),
            font=dict(
                family="sans-serif",
                size=12,
                color='white'),
        ),
    }

    df_category_wise_secondary_sales = get_service_category_wise_secondary_sales_data(0, '2021-10-01', '2021-10-31')
    df_cat_sorted = df_category_wise_secondary_sales.sort_values('SalesAmount')
    cat_name = df_cat_sorted['Category_Name']
    product_category_wise_sales = {
        'data': [go.Bar(x=df_cat_sorted['SalesAmount'],
                        y=df_cat_sorted['Category_Name'],
                        marker=dict(color='#3966FA'),
                        text=df_cat_sorted['SalesAmount'],
                        # hoverinfo='text',
                        hovertext=cat_name,
                        orientation='h'
                        ),
                 ],

        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            title={
                'text': 'Category Wise Sales',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 20},

            hovermode='y',
            margin=dict(r=2),
            xaxis=dict(title='Sales',
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

            yaxis=dict(title='',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=8,
                           color='white'
                       )
                       ),
            font=dict(
                family="sans-serif",
                size=12,
                color='white'),
        )
    }
    return month_wise_sales_data, day_wise_sales_data, product_wise_sales_data, product_category_wise_sales, attendance_data, stock_data





