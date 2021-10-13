# Dash app initialization
import dash
# User management initialization
import os
from flask_login import LoginManager, UserMixin
from users_mgt import db, User as base
from config import config


app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True

# config

server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# Create User class with UserMixin
class User(UserMixin, base):
    def __init__(self, id, username, email, fullname, admin):
        self.id = id
        self.username = username
        self.email = email
        self.fullname = fullname
        self.admin = admin



# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    usr = User.query.get(int(user_id))
    return User(usr.id, usr.username, usr.email, usr.fullname, usr.admin)