from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
from app import app
from apps import dbconnect as db



layout = html.Div(
    [
        html.H2('Reports'),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3('View Reports')
                    ]
                ),
                dbc.CardBody( 
                    [
                        html.Div(
                            [
                                html.Div(
                                    dbc.Form(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Label("Country", width=1),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            id='report_countryfilter',
                                                            placeholder='Select Country',
                                                            searchable=True,
                                                            options = [],
                                                            multi = True
                                                        ),
                                                        width=5
                                                    )
                                                ],
                                                className='mb-3'
                                            ),
                                        ],
                                    )
                                ),
                                html.Div([
                                    dcc.Loading(
                                        id="reportbodyload",
                                        children=[
                                        dcc.Graph(id='reportbodyreceipts',)
                                      ],type="circle")
                                ],style={'width':'100%',"border": "3px #5c5c5c solid",} ),
                                html.Hr(),
                                html.H5('Number of movies and actors per genre and country.'),
                                html.Div(
                                    id='report_movielist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


#callback to populate dropdown options
@app.callback(
    [
        Output('report_countryfilter', 'options'),
        
    ],
    [
        Input('url', 'pathname'),
    ]
)
def moviehome_loadmovielist(pathname):
    if pathname == '/reports/report':
        sql = """ SELECT country_name as label, 
                    country_id as value
                FROM countries
                WHERE country_delete_ind = %s
            """
        columns = ['label', 'value']
        values = [False]
        dfsql = db.getDataFromDB(sql, values, columns)
        return [dfsql.to_dict('records')]
    
    else:
        raise PreventUpdate


#callback for figure and table
@app.callback(
    [
        Output('report_movielist', 'children'),
        Output('reportbodyreceipts', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('report_countryfilter', 'value')
    ]
)
def moviehome_loadmovielist(pathname, filter_country):
    if pathname == '/reports/report':
        sql = """ SELECT g.genre_id,count(movie_name), country_name, genre_name, count(distinct(m.actor_id))
                FROM movies m
                    INNER JOIN genres g ON m.genre_id = g.genre_id
                    INNER JOIN actors a ON m.actor_id = a.actor_id
                    INNER JOIN countries c ON m.country_id = c.country_id
                WHERE movie_delete_ind = false
            """
        values = []
        
        if filter_country:
            sql += " AND c.country_id IN %s"
            values += [tuple(filter_country)]
        
        sql += """ Group By g.genre_id, country_name, genre_name
                    Order By country_name, genre_name
        """

        cols = ['ID', 'Number of Movies', 'Country Name', 'Genre', 'Number of Actors']

        df = db.getDataFromDB(sql, values, cols)

        
        df = df[['Genre','Country Name','Number of Movies','Number of Actors']]

        listofgenre = df["Genre"].unique().tolist()

    
        traces={}
        #setting up the values of the x-axis and y-axis of the Bar graph
        for genre in listofgenre:
            traces['tracebar_' + genre]=go.Bar(y=df[df["Genre"]==genre]["Number of Movies"],
                                    x=df[df["Genre"]==genre]["Country Name"],
                                    # orientation = 'h', #try to uncomment this line
                                    name=genre)
        
        #setting up the values of the x-axis and y-axis of the line chart
        for genre in listofgenre:
            traces['traceline_' + genre] = go.Scatter(y=df[df["Genre"]==genre]["Number of Actors"],
                                    x=df[df["Genre"]==genre]["Country Name"],
                                    # orientation = 'h', #try to uncomment this line
                                    mode = 'lines+markers',
                                    name=genre,
                                    yaxis='y2')
        
        #you can add more traces if you want!

        data=list(traces.values())

        #layout of the chart/graph
        layout = go.Layout(
                yaxis1={'categoryorder':'total ascending', 'title':"Number of Movies (y-axis for bar)",'range':[0,10]},
                yaxis2={'categoryorder':'total ascending', 'title':"Number of Actors (y-axis for line)",'overlaying':'y','side':'right', 'range':[0,10]},
                xaxis={'title':"Country", "mirror":False, "zeroline":True },
                height=500,
                width = 2000,
                margin={'b': 50,'t':20, 'l':175},
                hovermode='closest',
                autosize= False,
                dragmode = 'zoom',
                #bar graph
                barmode='stack', #try other barmodes (e.g. group)
                boxmode= "overlay",
                )


        figure3 = {'data':data, 'layout':layout }
        

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
        
        if df.shape[0]:
            return [table, figure3]
        else:
            return [table, go.Figure()]
    else:
        raise PreventUpdate
