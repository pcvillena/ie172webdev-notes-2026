
import webbrowser

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "My First Dash App"

app.layout = html.Div(
    [
        html.Div(
            'Hello World',
            style={'border': '2px dotted green', 
                   'text-align': 'center',
                   'margin': '2em', 
                   'padding': '5em'}
        ),
        
        html.Div(
            [
                html.Div("Box1", className='border'), 
                html.Div("Box2", className='border')
            ], 
            className='d-flex justify-content'
        )
    ]
)


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050', autoraise=True)
    app.run_server()