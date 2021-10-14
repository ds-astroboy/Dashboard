
import dash_bootstrap_components as dbc

from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

from app import app
from configuration.company_mgt import company_dropdown
from configuration.role_mgt import company_wise_role
from configuration.role_menu_mgt import add_role_menu




layout = dbc.Container([
    html.Br(),
    dbc.Container([
        dcc.Location(id='urlRoleMenu', refresh=True),
        html.H3('Add Role Menu'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Company: '),
                dcc.Dropdown(
                    id='company_dropdown',
                    style={
                        'width': '90%'
                    },
                    options=company_dropdown(),
                    clearable=False
                )], md=4),

            dbc.Col([
                dbc.Label('Role: '),
                dcc.Dropdown(
                    id='role_dropdown',
                    style={
                        'width': '90%'
                    },
                    options=[],
                    clearable=False
                )], md=8),

            # dbc.Col([
            # ], md=4),
        ]),
        dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    html.Button(
                        children='Create Role Menu',
                        id='createRoleMenuButton',
                        n_clicks=0,
                        type='submit',
                        className='btn btn-primary btn-lg'
                    ),
                    html.Br(),
                    html.Div(id='createRoleMenuSuccess')
                ], md=4),
        ])
    ], className='jumbotron'),

    dbc.Container([
        html.H3('View Menu Details'),
        # html.Hr(),
        # dbc.Row([
        # dbc.Col([
        #         dbc.Label('Menu: '),
        #         dcc.Dropdown(
        #             id='menu_dropdown',
        #             style={
        #                 'width': '90%'
        #             },
        #             options=[],
        #             clearable=False
        #         )], md=4),
        #         dbc.Col([
        #              html.Button('Add Row', id='editing-rows-button', n_clicks=0, className='btn btn-primary btn-lg')
        #            ], md=2)
        #         ]),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='datatable',
                    # columns=[
                    #     {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
                    # ],
                    data=[],
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                    page_size=10,
                ),
                # html.Div(id='datatable-interactivity-container')

        ], md=12),
        ]),
    ], className='jumbotron'),
])

@app.callback(
Output('role_dropdown', 'options'),
Input('company_dropdown', 'value'))
def get_role_option(company_dropdown):
    if company_dropdown:
        result = company_wise_role(company_dropdown)
        return [{'label': item['RoleName'], 'value': item['RoleId']} for item in result]
    else:
        return []


# @app.callback(
#     Output('adding-rows-table', 'data'),
#     Input('editing-rows-button', 'n_clicks'),
#     State('adding-rows-table', 'data'),
#     State('adding-rows-table', 'columns'),
#     State('menu_dropdown', 'label')
# )
# def add_row(n_clicks, rows, columns, menu_dropdown_value):
#     if n_clicks > 0:
#         print()
#         rows.append({col['id']: menu_dropdown_value, col['Menu Name']: "Test"} for col in columns)
#     return rows

# @app.callback(
# Output('datatable', 'columns'),
# Output('datatable', 'data'),
# Input('company_dropdown', 'value'))
# def update_datatable_data(company_dropdown_value):
#     if company_dropdown_value is None:
#         result = company_wise_menu(2)
#         df = pd.DataFrame(result)
#         df.set_index('id', inplace=True, drop=False)
#         return [{"name": i, "id": i} for i in df.columns], df.to_dict('records')
#     else:
#         result = company_wise_menu(company_dropdown_value)
#         df = pd.DataFrame(result)
#         df.set_index('id', inplace=True, drop=False)
#         return [{"name": i, "id": i} for i in df.columns], df.to_dict('records')



# @app.callback(
#     Output('datatable-interactivity-container', "children"),
#     Input('datatable-interactivity', "derived_virtual_data"),
#     Input('datatable-interactivity', "selected_row_ids"))
# def update_value(rows, derived_virtual_selected_rows):
#     if derived_virtual_selected_rows is None:
#         derived_virtual_selected_rows = []
#     return derived_virtual_selected_rows


@app.callback(Output('createRoleMenuSuccess', 'children'),
              [Input('createRoleMenuButton', 'n_clicks'),
              Input('datatable', "selected_row_ids"),
               State('company_dropdown', 'value'),
               State('role_dropdown', 'value'),
               ])
def createRoleMenu(n_clicks, menu_ids, company_id, role_id):
    if (n_clicks > 0) :
        if company_id > 0 and role_id > 0 and len(menu_ids) > 0:
            try:
                add_role_menu(company_id, role_id, menu_ids)
                return html.Div(children=['New role menu created'], className='text-success')
            except Exception as e:
                return html.Div(children=['New role menu created: {e}'.format(e=e)], className='text-danger')
        else:
            return html.Div(children=['Please input correctly'], className='text-danger')