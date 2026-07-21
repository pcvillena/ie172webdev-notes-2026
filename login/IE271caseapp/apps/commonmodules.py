# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app


# CSS Styling for the NavLink components
navlink_style = {
    'color': '#fff'
}

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("IE 271 Case App", className="ml-2")),
                ],
                align="center",
                className='g-0' # remove gutters (i.e. horizontal space between cols)
            ),
            href="/home",
        ),
        dbc.NavLink("Home", href="/home", style=navlink_style),
        dbc.NavLink("Movies", href="/movies", style=navlink_style),
        dbc.NavLink("Genres", href="/genres", style=navlink_style),
        dbc.NavLink("Logout", href="/logout", style=navlink_style),
    ],
    dark=True,
    color='dark'
)
