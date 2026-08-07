import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import logging

# Create the application object (stored in app variable), along with CSS stylesheets
app = dash.Dash(__name__, external_stylesheets=["assets/bootstrap.css", dbc.themes.BOOTSTRAP])

# Make sure that callbacks are not activated when input elements enter the layout
app.config.suppress_callback_exceptions = True
# Get CSS from a local folder
app.css.config.serve_locally = True
# Enables your app to run offline
app.scripts.config.serve_locally = True
# Set app title that appears in your browser tab
app.title = 'IE 271 Case'
# These 2 lines reduce the logs on your terminal so you could debug better
# when you encounter errors in app
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
