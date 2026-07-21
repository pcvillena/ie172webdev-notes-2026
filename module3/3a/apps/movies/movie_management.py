import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from app import app
from apps.dbconnect import getDataFromDB

layout = html.Div(
    [
        html.H2('Movies'), # Page Header
        html.Hr(),
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H3('Manage Records')
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Div( # Add Movie Btn
                            [
                                # Add movie button will work like a 
                                # hyperlink that leads to another page
                                dbc.Button(
                                    "Add Movie",
                                    href='/movies/movie_management_profile?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div( # Create section to show list of movies
                            [
                                html.H4('Find Movies'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Title", width=1),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='movie_titlefilter',
                                                        placeholder='Movie Title'
                                                    ),
                                                    width=5
                                                )
                                            ],
                                        )
                                    )
                                ),
                                html.Div(
                                    "Table with movies will go here.",
                                    id='movie_movielist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    [
        Output('movie_movielist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('movie_titlefilter', 'value'),
    ],
)
def updateRecordsTable(pathname, titlefilter):

    if pathname == '/movies/movie_management':
        pass
    else:
        raise PreventUpdate

    sql = """ SELECT movie_name, genre_name, to_char(movie_release_date, 'DD Mon YYYY'), 
        movie_id
    FROM movies m
        INNER JOIN genres g ON m.genre_id = g.genre_id
    WHERE NOT movie_delete_ind
    """
    val = []

    if titlefilter:
        sql += """ AND movie_name ilike %s"""
        val += [f'%{titlefilter}%']
    
    col = ["Movie Title", "Genre", "Release Date", 'id']

    df = getDataFromDB(sql, val, col)

    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                        href = f'/movies/movie_management_profile?mode=edit&id={row['id']}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]
    
    # we don't want to display the 'id' column -- let's exclude it
    df = df[['Movie Title', 'Genre', 'Release Date', 'Action']]

    movie_table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                        hover=True, size='sm')

    
    return [movie_table]