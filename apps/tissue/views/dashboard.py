
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, dash_table
import plotly.graph_objs as go

from app import app
from service_layer.AI_Services import *
from service_layer.services import get_service_marketchannel_stock, get_service_executive_count_data, get_service_all_division_attendance_data,\
    get_service_monthly_secondary_sales_data, get_service_date_wise_secondary_sales_data, get_service_product_wise_secondary_sales_data, \
    get_service_category_wise_secondary_sales_data, get_service_division_wise_secondary_sales_data
from common.dateinfo import *
from common.helpler import *
from helper.three_d_bar_chart_builder import *
import speech_recognition as sr

# https://dash.plotly.com/dash-core-components/graph
# https://pbpython.com/plotly-dash-intro.html
# https://bootswatch.com/flatly/    Bootstrap theme
# https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/ch04.html

# https://community.plotly.com/t/hyperlink-to-markers-on-map/17858   Hyperlink to markers on map

# https://resonance-analytics.com/blog/deploying-dash-apps-on-azure  deployment
# https://www.youtube.com/watch?v=x8xjj6cR9Nc     voice to text change
# https://www.tutorialspoint.com/plotly/plotly_with_matplotlib_and_chart_studio.htm  matplotlib to dash plotly convert

# https://github.com/AymericFerreira/Plotly_barchart3D       3D bar chart with source by github


layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Tissue Dashboard', style={'fontSize': 30}),
               ], className='text-white', style={'textAlign': 'center'})
        ]),
    ]),

    dbc.Row([
        dbc.Col([], md=4),
        dbc.Col([
            html.Div([
                dbc.Input(id="input_audio", placeholder="search by voice or text", className="form-control me-sm-2"),
                html.Img(id="button_audio", src=app.get_asset_url('mic.png'), n_clicks=0, width="50", height="37", className="btn btn-light"),
                html.Img(id="button_search", src=app.get_asset_url('search.png'), n_clicks=0, width="50", height="37", className="btn btn-light"),
            ], className="input-group mb-3")
         ], md=4),
         ]),
    dbc.Row(id="Div_Output"),
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
             # html.H4("Secondary Sales", style={"textAlign": "center"}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Graph(id='month_wise_sales', figure={}),
                                        html.Div([
                                            dcc.Link('MORE', href='/apps/tissue/views/salesorderoverview', target="_blank",className="btn btn-primary btn-lg"),
                                        ], style={'textAlign': 'right'}),
                                    ], className="create_container")
                                ]),
                            ], className="text-white"),
                        ], md=3, style={'textAlign': 'center'}),
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Graph(id='day_wise_sales', figure={}),
                                        html.Div([
                                            dcc.Link('MORE', href='/apps/tissue/views/salesorderoverview', target="_blank", className="btn btn-primary btn-lg"),
                                        ], style={'textAlign': 'right'}),
                                    ], className="create_container")
                                ]),
                            ], className="text-white"),
                        ], md=3, style={'textAlign': 'center'}),
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Graph(id='category_wise_sales', figure={}),
                                        html.Div([
                                            dcc.Link('MORE', href='/apps/tissue/views/salesorderoverview', target="_blank",  className="btn btn-primary btn-lg"),
                                        ], style={'textAlign': 'right'}),
                                    ], className="create_container")
                                ]),
                            ], className="text-white"),
                        ], md=3, style={'textAlign': 'center'}),

                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Graph(id='product_wise_sales', figure={}),
                                        html.Div([
                                            dcc.Link('MORE', href='/apps/tissue/views/salesorderoverview', target="_blank", className="btn btn-primary btn-lg"),
                                        ], style={'textAlign': 'right'}),
                                    ], className="create_container")
                                ]),
                            ], className="text-white"),
                        ], md=3, style={'textAlign': 'center'}),

                    ]),
                ], className="card-body")
            ], className="card-header")
        ], className="card text-white bg-primary")
       ])
   ]),
    dbc.Row([

        # dbc.Col([
        #     html.Div([
        #         html.Div([
        #             html.Div([
        #                 dcc.Graph(id='3d_bar_chart_sales', figure={}),
        #                 # html.Div([
        #                 #     dcc.Link('MORE', href='/apps/tissue/views/executiveattendance', target="_blank",
        #                 #              className="btn btn-primary btn-lg"),
        #                 # ], style={'textAlign': 'right'}),
        #             ], className="create_container")
        #         ]),
        #     ], className="text-white"),
        # ], md=4, style={'textAlign': 'center'}),

        dbc.Col([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='predictive_sales', figure={}),
                    ], className="create_container")
                ]),
            ], className="text-white"),
        ], md=6, style={'textAlign': 'center'}),

        dbc.Col([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='attendance_executive', figure={}),
                        html.Div([
                            dcc.Link('MORE', href='/apps/tissue/views/executiveattendance', target="_blank", className="btn btn-primary btn-lg"),
                        ], style={'textAlign': 'right'}),
                    ], className="create_container")
                ]),
            ], className="text-white"),
        ], md=3, style={'textAlign': 'center'}),

        dbc.Col([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='stock', figure={}),
                        html.Div([
                            dcc.Link('MORE', href='/apps/tissue/views/productstocksummary', target="_blank", className="btn btn-primary btn-lg"),
                        ], style={'textAlign': 'right'}),
                    ], className="create_container")
                ]),
            ], className="text-white"),
        ], md=3, style={'textAlign': 'center'}),

    ]),

    # dbc.Row([
    #      dbc.Col([
    #         html.Div([
    #             html.Div([
    #                 html.Div([
    #                     html.Iframe(src="http://10.10.83.69:8080/3DModel", width=500, height=500),
    #                 ], className="create_container")
    #             ]),
    #         ], className="text-white"),
    #     ], md=4, style={'textAlign': 'center'}),
    #
    #     dbc.Col([
    #         html.Div([
    #             html.Div([
    #                 html.Div([
    #                     dcc.Graph(id='division_sales', figure={}),
    #                     # html.Div([
    #                     #     dcc.Link('MORE', href='/apps/tissue/views/executiveattendance', target="_blank",
    #                     #              className="btn btn-primary btn-lg"),
    #                     # ], style={'textAlign': 'right'}),
    #                 ], className="create_container")
    #             ]),
    #         ], className="text-white"),
    #     ], md=4, style={'textAlign': 'center'}),
    #  ])
])
def get_division_wise_sales():
    start_date = '2021-12-01'
    end_date = '2021-12-31'
    df_category_wise_secondary_sales = get_service_division_wise_secondary_sales_data(start_date, end_date)
    df_division_sorted = df_category_wise_secondary_sales.sort_values('SalesAmount')
    div_name = df_division_sorted['Name']

    division_wise_sales = {
        'data': [go.Bar(x=df_division_sorted['SalesAmount'],
                            y=df_division_sorted['Name'],
                            marker=dict(color='#009999'),
                            text=df_division_sorted['SalesAmount'],
                            texttemplate='%{text:.2s}',
                            # hoverinfo='text',
                            hovertext=div_name,
                            orientation='h'
                            ),
                     ],

        'layout': go.Layout(
                plot_bgcolor='#1f2c56',
                paper_bgcolor='#1f2c56',
                title={
                    'text': 'Division Wise Sales',
                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'white',
                    'size': 20},

                hovermode='y',
                margin=dict(r=2),
                xaxis=dict(title='',
                           color='white',
                           showline=True,
                           showgrid=True,
                           showticklabels=False,
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
    return division_wise_sales

def get_category_sales(start_date, end_date, param, is_voice_call=False):
    product_category_wise_sales = {}
    df_category_wise_secondary_sales = get_service_category_wise_secondary_sales_data(start_date, end_date)
    df_cat_sorted = df_category_wise_secondary_sales.sort_values('SalesAmount')
    cat_name = df_cat_sorted['Category_Name']
    if 'bar' in param:
        product_category_wise_sales = {
            'data': [go.Bar(x=df_cat_sorted['SalesAmount'],
                            y=df_cat_sorted['Category_Name'],
                            marker=dict(color='#009999'),
                            text=df_cat_sorted['SalesAmount'],
                            texttemplate='%{text:.2s}',
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
                xaxis=dict(title='',
                           color='white',
                           showline=True,
                           showgrid=True,
                           showticklabels=False,
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
    elif 'pie' in param:
        product_category_wise_sales = {
            'data': [go.Pie(labels=df_cat_sorted['Category_Name'],
                            values=df_cat_sorted['SalesAmount'],
                            marker=dict(colors=df_cat_sorted['Category_Name']),
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
                    'text': 'Category Sales',
                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'white',
                    'size': 25},
                # legend={
                #     'orientation': 'h',
                #     'bgcolor': '#1f2c56',
                #     'xanchor': 'center', 'x': 0.5, 'y': -0.07},
                font=dict(
                    family="sans-serif",
                    size=15,
                    color='white')
            ),

        }
    elif '3d_chart' in param:
        product_category_wise_sales = {
            plotly_barcharts_3d(df_cat_sorted['Category_Name'], df_cat_sorted['SalesAmount'], df_cat_sorted['SalesAmount'], color=df_cat_sorted['Category_Name'])
        }
    if is_voice_call is True:
        content = []
        content.append(dbc.Col([], md=4))
        content.append(dbc.Col([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='category_sales_'+param, figure=product_category_wise_sales),
                        html.Div([
                            dcc.Link('MORE', href='/apps/tissue/views/salesorderoverview', target="_blank",
                                     className="btn btn-primary btn-lg"),
                        ], style={'textAlign': 'right'}),
                    ], className="create_container")
                ]),
            ], className="text-white"),
        ], md=6, style={'textAlign': 'center'}))
        return content
    else:
        return product_category_wise_sales

def get_product_sales(start_date, end_date, param, is_voice_call = False):
    product_wise_sales_data = {}
    df_product_wise_secondary_sales = get_service_product_wise_secondary_sales_data(start_date, end_date)
    df_sorted = df_product_wise_secondary_sales.sort_values('SalesAmount')
    if 'bar' in param:
        product_wise_sales_data = {
            'data': [go.Bar(x=df_sorted['SalesAmount'],
                            y=df_sorted['ProductName'],
                            marker=dict(color='#319177'),
                            text=df_sorted['SalesAmount'],
                            texttemplate='%{text:.2s}',
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
                xaxis=dict(title='',
                           color='white',
                           showline=True,
                           showgrid=True,
                           showticklabels=False,
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
    elif 'pie' in param:
        product_wise_sales_data = {
            'data': [go.Pie(labels=df_sorted['ProductName'],
                            values=df_sorted['SalesAmount'],
                            marker=dict(colors=df_sorted['ProductName']),
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
                    'text': 'Category Sales',
                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'white',
                    'size': 25},
                # legend={
                #     'orientation': 'h',
                #     'bgcolor': '#1f2c56',
                #     'xanchor': 'center', 'x': 0.5, 'y': -0.07},
                font=dict(
                    family="sans-serif",
                    size=15,
                    color='white')
            ),

        }
    if is_voice_call is True:
        content = []
        content.append(dbc.Col([], md=4))
        content.append(dbc.Col([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='product_sales_' + param, figure=product_wise_sales_data),
                        html.Div([
                            dcc.Link('MORE', href='/apps/tissue/views/salesorderoverview', target="_blank",
                                     className="btn btn-primary btn-lg"),
                        ], style={'textAlign': 'right'}),
                    ], className="create_container")
                ]),
            ], className="text-white"),
        ], md=6, style={'textAlign': 'center'}))
        return content
    else:
        return product_wise_sales_data

def get_today_sales(param):
    content = []
    output_data = 600000
    content.append(dbc.Col([], md=4))
    content.append(
        dbc.Col([
            html.Div([
                dbc.Input(id="sales_data_"+param, className="form-control", value=output_data),
            ], className="input-group mb-3")
        ], md=4))
    return content

def get_lastday_sales(param):
    content = []
    output_data = 500000
    content.append(dbc.Col([], md=4))
    content.append(
        dbc.Col([
            html.Div([
                dbc.Input(id="sales_data_"+param, className="form-control", value=output_data),
            ], className="input-group mb-3")
        ], md=4))
    return content

def get_all_voice_command():
    content = []
    command_list = [
                    {'SL': 1, 'Command': 'all voice commands'},
                    {'SL': 2, 'Command': '''today's sales'''},
                    {'SL': 3, 'Command': '''last day's sales'''},
                    {'SL': 4, 'Command': 'all voice commands'},
                    {'SL': 5, 'Command': 'category bar chart'},
                    {'SL': 6, 'Command': 'category pie chart'},
                    {'SL': 7, 'Command': 'product bar chart'},
                    {'SL': 8, 'Command': 'product pie chart'}
                   ]
    df = pd.DataFrame(command_list)
    content.append(dbc.Col([], md=4))
    content.append(dbc.Col([
        html.Div([
            html.Div([
                html.Div([
                    dash_table.DataTable(id='datatable_voice_command',
                                         columns=[{"name": i, "id": i} for i in df.columns],
                                         data=df.to_dict('records'),
                                         fixed_rows={'headers': True},
                                         style_table={'height': 400},
                                         style_header={
                                             'backgroundColor': '#1f2c56',
                                             'color': 'white',
                                             'fontWeight': 'bold'
                                         },
                                         style_data_conditional=[{
                                             'if': {'column_editable': False},
                                             'backgroundColor': '#1f2c56',
                                             'color': 'white'
                                         }],
                                         ),
                ], className="create_container")
            ]),
        ], className="text-white"),
    ], md=4, style={'textAlign': 'center'}))
    return content

def get_no_match_found():
    content = []
    content.append(dbc.Col([], md=4))
    content.append(
        dbc.Col([
            html.Div([
                dbc.Input(id="match_data", className="form-control", value='no match found'),
            ], className="input-group mb-3")
        ], md=4))
    return content

def respond(voice_data):
    from_date = '2021-12-01'
    to_date = '2021-12-31'
    if voice_data:
        if 'today sales' in voice_data or '''today's sales''' in voice_data:
            result = get_today_sales('today')
            return result
        elif 'last day sales' in voice_data or '''last day's sales''' in voice_data:
            result = get_lastday_sales('lastday')
            return result
        elif 'category sales 3d bar chart' in voice_data or 'category wise sales 3d bar chart' in voice_data or 'category 3d bar chart' in voice_data:
            result = get_category_sales(from_date, to_date, '3d_chart', True)
            return result
        elif 'category sales bar chart' in voice_data or 'category wise sales bar chart' in voice_data or 'category bar chart' in voice_data:
            result = get_category_sales(from_date, to_date, 'bar', True)
            return result
        elif 'category sales pie chart' in voice_data or 'category wise sales pie chart' in voice_data or 'category pie chart' in voice_data:
            result = get_category_sales(from_date, to_date, 'pie', True)
            return result

        elif 'product sales bar chart' in voice_data or 'product wise sales bar chart' in voice_data or 'product bar chart' in voice_data:
            result = get_product_sales(from_date, to_date, 'bar', True)
            return result
        elif 'product sales pie chart' in voice_data or 'product wise sales pie chart' in voice_data or 'product pie chart' in voice_data:
            result = get_product_sales(from_date, to_date, 'pie', True)
            return result
        elif 'all voice commands' in voice_data or 'all voice command' in voice_data:
            result = get_all_voice_command()
            return result
        else:
            result = get_no_match_found()
            return result
    else:
        return ''

def record_data():
    voice_data = ''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            return 'Sorry, I did not get that'
        except sr.RequestError:
            return 'Sorry, speech service is down'
        return voice_data.lower()

# voice search
@app.callback(
    Output('input_audio', 'value'),
    Output('Div_Output', 'value'),
    Input('button_audio', 'n_clicks')
)

def update_dashboard(n_clicks):
    voice_data = ''
    output_data = ''
    if n_clicks > 0:
        voice_data = record_data()
        output_data = respond(voice_data)
    return voice_data, output_data

#direct search
@app.callback(
    Output('Div_Output', 'children'),
    Input('button_search', 'n_clicks'),
    Input('input_audio', 'value')
)

def update_dashboard(n_clicks, value):
    output_data = ''
    output_content = []
    if n_clicks > 0:
        output_content = respond(value.lower())
    return output_content


@app.callback(

    Output('month_wise_sales', 'figure'),
    Output('day_wise_sales', 'figure'),

    Output('category_wise_sales', 'figure'),
    Output('product_wise_sales', 'figure'),
    # Output('3d_bar_chart_sales', 'figure'),
    Output('attendance_executive', 'figure'),
    Output('stock', 'figure'),
    Output('predictive_sales', 'figure'),
    # Output('division_sales', 'figure'),

    Input('start_date', 'date'),
    # Input('end_date', 'date'),

)

def update_dashboard(start_date):

    start_date = '2022-04-10'
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
                        texttemplate='%{text:.2s}',
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
            xaxis=dict(title='',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=False,
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

    stock_df = get_service_marketchannel_stock(start_date, end_date)
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
    df = get_service_date_wise_secondary_sales_data('2022-06-01', '2022-06-10')
    df_sales = df.groupby(["OrderDate"], as_index=False)["SalesAmount"].sum()
    day_wise_sales_data = {
        'data': [go.Bar(x=df_sales['SalesAmount'],
                        y=df_sales['OrderDate'],
                        marker=dict(color='#0099cc'),
                        text=df_sales['SalesAmount'],
                        texttemplate='%{text:.2s}',
                        # hoverinfo='text',
                        # hovertext=''
                        orientation='h'
                        ),
                 ],
        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            title={
                'text': 'Last 10 days Sales',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 20},

            hovermode='y',
            margin=dict(r=0),
            xaxis=dict(title='',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=False,
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
    from_date = '2022-04-01'
    to_date = '2022-04-30'
    product_category_wise_sales = get_category_sales(from_date, to_date, 'bar')
    product_wise_sales_data = get_product_sales(from_date, to_date, 'bar')
    # features = [2, 3, 5, 10, 20]
    # neighbours = [31, 24, 10, 28, 48]
    # accuracies = [0.9727, 0.9994, 0.9994, 0.9995, 0.9995]
    # plotly_barcharts_3d(features, neighbours, accuracies, x_title="Features", y_title="Neighbours", z_title="Accuracy").show()

    # xdf = pd.Series([1, 10])
    # ydf = pd.Series([2, 4])
    # zdf = pd.Series([10, 30, 20, 45])
    # three_d_fig = plotly_barcharts_3d(xdf, ydf, zdf, color='x+y')

    # three_d_fig = get_category_sales(0, from_date, to_date, '3d bar')

    predictive_sales_data = get_AI_service_monthly_secondary_sales_data()

    # predictive_sales_data = {
    #     'data': [go.Line(predictive_sales, x='OrderDate', y='SalesAmount',
    #                     # marker=dict(color='#0099cc'),
    #                     # text=df_sales['SalesAmount'],
    #                     # texttemplate='%{text:.2s}',
    #                     # hoverinfo='text',
    #                     # hovertext=''
    #                     # orientation='h'
    #                     ),
    #              ],
    #     'layout': go.Layout(
    #         plot_bgcolor='#1f2c56',
    #         paper_bgcolor='#1f2c56',
    #         title={
    #             'text': 'Day Wise Sales',
    #             'y': 0.93,
    #             'x': 0.5,
    #             'xanchor': 'center',
    #             'yanchor': 'top'},
    #         titlefont={
    #             'color': 'white',
    #             'size': 20},
    #
    #         hovermode='y',
    #         margin=dict(r=0),
    #         xaxis=dict(title='',
    #                    color='white',
    #                    showline=True,
    #                    showgrid=True,
    #                    showticklabels=False,
    #                    linecolor='white',
    #                    linewidth=2,
    #                    ticks='outside',
    #                    tickfont=dict(
    #                        family='Arial',
    #                        size=12,
    #                        color='white'
    #                    )
    #                    ),
    #
    #         yaxis=dict(title='Day',
    #                    color='white',
    #                    showline=True,
    #                    showgrid=True,
    #                    showticklabels=True,
    #                    linecolor='white',
    #                    linewidth=2,
    #                    ticks='outside',
    #                    tickfont=dict(
    #                        family='Arial',
    #                        size=12,
    #                        color='white'
    #                    )
    #                    ),
    #         font=dict(
    #             family="sans-serif",
    #             size=12,
    #             color='white'),
    #     )
    # }
    # predictive_sales_data = px.line(predictive_sales, x="OrderDate", y="SalesAmount")
    predictive_sales = predictive_sales_data.sort_values('Year_Month')
    predictive_sales_data = {
        'data': [
            # go.Bar(x=df_sales['OrderDate'],
            #             y=df_sales['TotalOrderPrice'],
            #             marker=dict(color='orange'),
            #             # hoverinfo='text',
            #             # hovertext=''
            #             ),
                 go.Scatter(x=predictive_sales['Month_Year'],
                            y=predictive_sales['SalesAmount'],
                            mode='lines',
                            name='',
                            line=dict(width=3, color='#FF00FF'),
                            marker=dict(color='green'),
                            hoverinfo='text',
                            hovertext=predictive_sales['SalesAmount']
                            )
                 ],

        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            title={
                'text': 'AI powered monthly predictive sales',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 20},

            hovermode='x',
            margin=dict(r=0),
            xaxis=dict(title='Month',
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
    # division_wise_sales = get_division_wise_sales() \

    return month_wise_sales_data\
        , day_wise_sales_data, product_category_wise_sales, product_wise_sales_data\
        , attendance_data, stock_data, predictive_sales_data
    # , division_wise_sales





