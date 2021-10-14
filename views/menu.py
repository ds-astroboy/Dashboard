
import dash_bootstrap_components as dbc
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
from app import app
from configuration.role_mgt import show_roles, add_role
from configuration.company_mgt import company_dropdown


layout = dbc.Container([
    html.Br(),
    dbc.Container([
        dcc.Location(id='urlRole', refresh=True),
        html.H3('Add Role'),
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
           html.Br(),
            dbc.Col([
                dbc.Label('Menu: '),
                dcc.Input(
                    id='newMenuname',
                    className='form-control',
                    n_submit=0,
                    style={
                        'width': '90%'
                    },
                ),
            ], md=4),
            dbc.Col([
            ], md=4)
        ]),

        dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    html.Button(
                        children='Create Menu',
                        id='createMenuButton',
                        n_clicks=0,
                        type='submit',
                        className='btn btn-primary btn-lg'
                    ),
                    html.Br(),
                    html.Div(id='createMenuSuccess')
                ], md=4),
        ])
    ], className='jumbotron'),

    dbc.Container([
        html.H3('View Menus'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dt.DataTable(
                    id='roles',
                    columns=[{'name': 'ID', 'id': 'RoleId'},
                            {'name': 'Role', 'id': 'RoleName'},
                            {'name': 'Company', 'id': 'CompanyName'}
                          ],
                    data=show_roles(),
                ),
            ], md=12),
        ]),
    ], className='jumbotron')
])

# CREATE ROLE BUTTON CLICK / FORM SUBMIT - VALIDATE ROLENAME
@app.callback(Output('newMenuname', 'className'),
              [
              Input('createMenuButton', 'n_clicks'),
              Input('newMenuname', 'n_submit')
              ],
              [State('newMenuname', 'value')])

def validateMenuname(n_clicks, menunameSubmit,newMenuename):

    if (n_clicks > 0) or (menunameSubmit > 0):

        if newMenuename == None or newMenuename == '':
            return 'form-control is-invalid'
        else:
            return 'form-control is-valid'
    else:
        return 'form-control'

# @app.callback(Output('company_dropdown', 'className'),
#               [
#               Input('createRoleButton', 'n_clicks'),
#               Input('company_dropdown', 'n_submit')
#               ],
#               [State('company_dropdown', 'value')])
#
# def validateCompanyname(n_clicks,companyNameSubmit, company_dropdown):
#     if (n_clicks > 0):
#         if company_dropdown == None or company_dropdown == '':
#             return 'form-control is-invalid'
#         else:
#             return 'form-control is-valid'
#     else:
#         return 'form-control'

@app.callback(Output('createMenuSuccess', 'children'),
              [Input('createMenuButton', 'n_clicks'),
              Input('newMenuname', 'n_submit'),
              Input('company_dropdown', 'n_submit'),
              State('newMenuname', 'value'),
              State('company_dropdown', 'value')
               ])

def createRole(n_clicks, roleSubmit, companySubmit, roleName,  company_id):
    if (n_clicks > 0) :
        if len(roleName) > 2 and company_id > 0:
            try:
                add_role(roleName, company_id)
                return html.Div(children=['New Role created'], className='text-success')
            except Exception as e:
                return html.Div(children=['Role not created: {e}'.format(e=e)], className='text-danger')
        else:
            return html.Div(children=['Role Name Must Be Minimum 3 Characters'], className='text-danger')