
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc


from app import app, server
from flask_login import logout_user, current_user
from views import login, error, default, page2, profile, user_admin, role, role_menu
from apps.tissue.views import test, productoverview, salesorderoverview, productstocksummary, executiveattendance, dashboard,topsale, customdashboard
from config import conn_security


# https://auth0.com/docs/quickstart/backend/python/01-authorization#configure-auth0-apis

navBar = dbc.Navbar(id='navBar',
    children=[],
    sticky='top',
    color='primary',
    className='navbar navbar-expand-lg navbar-dark bg-primary',
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        navBar,
        html.Div(id='pageContent')
    ])
], id='table-wrapper')


################################################################################
# HANDLE PAGE ROUTING - IF USER NOT LOGGED IN, ALWAYS RETURN TO LOGIN SCREEN
################################################################################
@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def displayPage(pathname):
    if pathname == '/':
        if current_user.is_authenticated:
            return default.layout
        else:
            return login.layout

    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            return login.layout

    if pathname.lower() == '/apps/tissue/views/dashboard':
        return dashboard.layout
        # if current_user.is_authenticated:
        #     return dashboard.layout
        # else:
        #     return login.layout
        
    # if pathname.lower() == '/page3':
    #     if current_user.is_authenticated:
    #         return crm.crm_dash
    #     else:
    #         return login.layout
    # if pathname == '/page2':
    #     if current_user.is_authenticated:
    #         return crm.crm_dash
    #     else:
    #         return login.layout

    if pathname == '/role':
        if current_user.is_authenticated:
            return role.layout
        else:
            return login.layout

    if pathname == '/role_menu':
        if current_user.is_authenticated:
            return role_menu.layout
        else:
            return login.layout

    if pathname == '/apps/tissue/views/viewsproductoverview':
        return productoverview.layout
        # if current_user.is_authenticated:
        #     return productoverview.layout
        # else:
        #     return login.layout

    if pathname == '/apps/tissue/views/salesorderoverview':
        return salesorderoverview.layout
        # if current_user.is_authenticated:
        #     return salesorderoverview.layout
        # else:
        #     return login.layout

    if pathname == '/apps/tissue/views/productstocksummary':
        return productstocksummary.layout
        # if current_user.is_authenticated:
        #     return productstocksummary.layout
        # else:
        #     return login.layout

    if pathname == '/apps/tissue/views/executiveattendance':
        return executiveattendance.layout
        # if current_user.is_authenticated:
        #     return executiveattendance.layout
        # else:
        #     return login.layout

    # if pathname == '/dashboard':
    #     if current_user.is_authenticated:
    #         return dashboard.layout
    #     else:
    #         return login.layout

    if pathname == '/customdashboard':
        if current_user.is_authenticated:
            return customdashboard.layout
        else:
            return login.layout

    if pathname == '/topsale':
        if current_user.is_authenticated:
            return topsale.layout
        else:
            return login.layout
    if pathname == '/profile':
        return profile.layout
        # if current_user.is_authenticated:
        #     return profile.layout
        # else:
        #     return login.layout

    if pathname == '/admin':
        return user_admin.layout
        # if current_user.is_authenticated:
        #     if current_user.admin == 1:
        #         return user_admin.layout
        #     else:
        #         return error.layout
        # else:
        #     return login.layout

    else:
        return error.layout

################################################################################
@app.callback(
    Output('navBar', 'children'),
    [Input('pageContent', 'children')])
def navBar(input1):
    if current_user.is_authenticated:
        if current_user.admin == 1:

            child_tissue = []
            child_Config = []
            tisse_menu = ''
            config_menu = ''

            user_id = current_user.id
            cursor = conn_security.cursor()
            stored_proc = f"exec spGetUserMenu @Id = {user_id}"
            cursor.execute(stored_proc)
            result = list(cursor.fetchall())
            # user_menus = list(result)


            for item in result:
                if item[6] == 'Config':
                    appended_item = dbc.DropdownMenuItem('{}'.format(item[7]), href='{}'.format(item[8]))
                    child_Config.append(appended_item)
                elif item[6] == 'Tissue':
                    appended_item = dbc.DropdownMenuItem('{}'.format(item[7]), href='{}'.format(item[8]))
                    child_tissue.append(appended_item)
                else:
                    pass

            if len(child_tissue) > 0:
                tisse_menu = dbc.DropdownMenu(
                            nav=True,
                            in_navbar=True,
                            label="Tissue",
                            children=child_tissue
                        )
            if len(child_Config) > 0:
                config_menu = dbc.DropdownMenu(
                            nav=True,
                            in_navbar=True,
                            label="Configuration",
                            children=child_Config
                        )
            navBarContents = [
                     tisse_menu,
                     config_menu,
                     dbc.DropdownMenu(
                        nav=True,
                        in_navbar=True,
                        label=current_user.username,
                        children=[
                            dbc.DropdownMenuItem('Profile', href='/profile'),
                            dbc.DropdownMenuItem('Admin', href='/admin'),
                            dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem('Logout', href='/logout'),
                        ],
                    ),
                ]
            return navBarContents

        else:

            child_tissue = []
            child_Config = []
            tisse_menu = ''
            config_menu = ''

            user_id = current_user.id
            cursor = conn_security.cursor()
            stored_proc = f"exec spGetUserMenu @Id = {user_id}"

            cursor.execute(stored_proc)
            result = cursor.fetchall()
            user_menus = list(result)

            for item in user_menus:
                if item[6] == 'Config':
                    appended_item = dbc.DropdownMenuItem('{}'.format(item[7]), href='{}'.format(item[8]))
                    child_Config.append(appended_item)
                elif item[6] == 'Tissue':
                    appended_item = dbc.DropdownMenuItem('{}'.format(item[7]), href='{}'.format(item[8]))
                    child_tissue.append(appended_item)
                else:
                    pass

            if len(child_tissue) > 0:
                tisse_menu = dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label="Tissue",
                    children=child_tissue
                )
            if len(child_Config) > 0:
                config_menu = dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label="Configuration",
                    children=child_Config
                )
            navBarContents = [
                    tisse_menu,
                    config_menu,
                    dbc.DropdownMenu(
                        nav=True,
                        in_navbar=True,
                        label=current_user.username,
                        children=[
                            dbc.DropdownMenuItem('Profile', href='/profile'),
                            dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem('Logout', href='/logout'),
                        ],
                    ),
                ]
            return navBarContents

    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)