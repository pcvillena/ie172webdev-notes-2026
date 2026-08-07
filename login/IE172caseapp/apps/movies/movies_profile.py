# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from urllib.parse import urlparse, parse_qs

# Let us import the app object in case we need to define
# callbacks here
from app import app
#for DB needs
from apps import dbconnect as db

# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.Div( # This div shall contain all dcc.Store objects
            [
                dcc.Store(id='movieprofile_toload', storage_type='memory', data=0),
            ]
        ),

        html.H2('Movie Details'), # Page Header
        html.Hr(),
        dbc.Alert(id='movieprofile_alert', is_open=False), # For feedback purposes
        dbc.Form(
            [
                # Form fields here
                dbc.Row(
                    [
                        dbc.Label("Title", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='movieprofile_title',
                                placeholder="Title"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3' # add 1em bottom margin
                ),
                dbc.Row(
                    [
                        dbc.Label("Genre", width=1),
                        dbc.Col(
                            dcc.Dropdown(
                                id='movieprofile_genre',
                                placeholder='Genre'
                            ),
                            width=5
                        )
                    ],
                    className='mb-3' # add 1em bottom margin
                ),
                dbc.Row(
                    [
                        dbc.Label("Release Date", width=1),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='movieprofile_releasedate',
                                placeholder='Release Date',
                                month_format='MMM Do, YY',
                            ),
                            width=5
                        )
                    ],
                    className='mb-3' # add 1em bottom margin
                ),

            ]
        ),
        # enclosing the checklist in a Div so we can
        # hide it in Add Mode
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='movieprofile_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            # I want the label to be bold
                            style={'fontWeight':'bold'}, 
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            id='movieprofile_removerecord_div'
        ),

        dbc.Button(
            'Submit',
            id='movieprofile_submit',
            n_clicks=0 # Initialize number of clicks
        ),
        dbc.Modal( # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    'Message here! Edit me please!'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/movies' # Clicking this would lead to a change of pages
                    )
                )
            ],
            centered=True,
            id='movieprofile_successmodal',
            backdrop='static' # Dialog box does not go away if you click at the background
        )
    ]
)


@app.callback(
    [
        Output('movieprofile_genre', 'options'),
        Output('movieprofile_toload', 'data'),
        Output('movieprofile_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') # add this search component to the State
    ]
)
def movieprof_loaddropdown(pathname, search):
    
    if pathname == '/movies/movies_profile':
        sql = """
            SELECT genre_name as label, genre_id as value
            FROM genres
            WHERE genre_delete_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        genre_opts = df.to_dict('records')
        
        # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0

        # to show the remove option?

        removediv_style = {'display': 'none'} if not to_load else None
        # if to_load = 0, then not to_load -> not 0 -> not False -> True

    
    else:
        raise PreventUpdate

    return [genre_opts, to_load, removediv_style]




@app.callback(
    [
        # dbc.Alert Properties
        Output('movieprofile_alert', 'color'),
        Output('movieprofile_alert', 'children'),
        Output('movieprofile_alert', 'is_open'),
        # dbc.Modal Properties
        Output('movieprofile_successmodal', 'is_open')
    ],
    [
        # For buttons, the property n_clicks 
        Input('movieprofile_submit', 'n_clicks')
    ],
    [
        # The values of the fields are States 
        # They are required in this process but they 
        # do not trigger this callback
        State('movieprofile_title', 'value'),
        State('movieprofile_genre', 'value'),
        State('movieprofile_releasedate', 'date'),
        State('url', 'search'), # we need this to identify which mode we are in
        State('movieprofile_removerecord', 'value'),
    ]
)
def movieprofile_saveprofile(submitbtn, title, genre, releasedate,
                             search, removerecord):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'movieprofile_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout

            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            # We need to check inputs
            if not title: # If title is blank, not title = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the movie title.'
            elif not genre:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the movie genre.'
            elif not releasedate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the movie release date.'
            else: # all inputs are valid

                # parse or decode the 'mode' portion of the search queries 
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                if create_mode == 'add':
                    # Add the data into the db
                    # save to db

                    sql = '''
                        INSERT INTO movies (movie_name, genre_id,
                            movie_release_date, movie_delete_ind)
                        VALUES (%s, %s, %s, %s)
                    '''
                    values = [title, genre, releasedate, False]

                    db.modifydatabase(sql, values)
                    

                elif create_mode == 'edit':
                    # 1. we need to get the movieid to update
                    parsed = urlparse(search)
                    movieid = parse_qs(parsed.query)['id'][0]

                    # 2. we need to update the db
                    sqlcode = """UPDATE movies
                    SET
                        movie_name = %s,
                        genre_id = %s,
                        movie_release_date  = %s,
                        movie_delete_ind = %s
                    WHERE
                        movie_id = %s
                    """
                    to_delete = bool(removerecord)
                    values = [title, genre, releasedate, to_delete,
                              movieid]

                    db.modifydatabase(sqlcode, values)

                    # If this is successful, we want the successmodal to show
                    modal_open = True


            return [alert_color, alert_text, alert_open, modal_open]

        else: # Callback was not triggered by desired triggers
            raise PreventUpdate

    else:
        raise PreventUpdate


@app.callback(
    [
        # Our goal is to update values of these fields
        Output('movieprofile_title', 'value'),
        Output('movieprofile_genre', 'value'),
        Output('movieprofile_releasedate', 'date'),
    ],
    [
        # Our trigger is if the dcc.Store object changes its value
        # This is how you check a change in value for a dcc.Store
        Input('movieprofile_toload', 'modified_timestamp')
    ],
    [
        # We need the following to proceed
	    # Note that the value of the dcc.Store object is in
	    # the ‘data’ property, and not in the ‘modified_timestamp’ property
        State('movieprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def movieprofile_loadprofile(timestamp, toload, search):
    if toload: # check if toload = 1
        
        # Get movieid value from the search parameters
        parsed = urlparse(search)
        movieid = parse_qs(parsed.query)['id'][0]

        # Query from db
        sql = """
            SELECT movie_name, genre_id, movie_release_date
            FROM movies
            WHERE movie_id = %s
        """
        values = [movieid]
        col = ['moviename', 'genreid', 'releasedate']

        df = db.querydatafromdatabase(sql, values, col)

        moviename = df['moviename'][0]
        # Our dropdown list has the genreids as values then it will 
        # display the correspoinding labels
        genreid = int(df['genreid'][0])
        releasedate = df['releasedate'][0]

        return [moviename, genreid, releasedate]

    else:
        raise PreventUpdate
