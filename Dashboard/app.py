# -*- coding: utf-8 -*-
# Import required libraries
import pandas as pd
import numpy as np
import dash
import pathlib
import plotly
import random
import collections
import plotly
import random
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import multiprocessing
import time
import sys
import serial
from ast import literal_eval


WINDOW_SIZE = 150
UPDATE_INTERVAL = 500


# Setup the app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()


app.layout = html.Div(
    [
        dcc.Store(id="click-output"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url("vein-logo.png"),
                                    className="plotly-logo",
                                )
                            ]
                        ),
                        dcc.Markdown(
                            """### A Wearable For The Lifter""".replace("  ", ""),
                            className="title",
                        )
                    ]
                ),
                html.Div(
                    [
                    html.Div([
                        html.Div([dcc.Markdown(id="prediction-text")]),
                        dcc.Graph(id="bargraph-confidence", animate=True, style={"margin": "0px 0px", "height":"30vh"}),
                        ], 
                        className="subtitle", style={"margin": "60px 0px"}),
                    dcc.Interval(
                        id='pred_update',                 
                        interval=1000, # in milliseconds
                        n_intervals=0),
                    ],
                ),
                html.Div(
                    [
                    html.Div([
                        html.Div([dcc.Markdown(id="repetitions-text")])
                        ], 
                        className="subtitle", style={"margin": "0px 0px"}),
                    dcc.Interval(
                        id='reps_update',                 
                        interval=UPDATE_INTERVAL, # in milliseconds
                        n_intervals=0),
                    ],
                ),
            ],
            className="four columns sidebar",
        ),
        html.Div(
            [
                html.Div(
                    [
                    dcc.Graph(id='Yaw', style={"margin": "20px 0px", "height": "30vh"}),   
                    dcc.Interval(
                        id='update-graphs',
                        interval=UPDATE_INTERVAL, # in milliseconds
                        n_intervals=0
                    ),
                    dcc.Graph(id='Pitch', style={"margin": "0px 0px", "height":"30vh"}),
                    dcc.Graph(id='Roll', style={"margin": "0px 0px", "height": "30vh"}),
                    ],
                    className="column", style={"width": "50%", "float": "left"}
                ),
                html.Div(
                    [
                    dcc.Graph(id='XAccel', style={"margin": "20px 0px", "height": "30vh"}),   
                    dcc.Graph(id='YAccel', style={"margin": "0px 0px", "height":"30vh"}),
                    dcc.Graph(id='ZAccel', style={"margin": "0px 0px", "height": "30vh"}),
                    ],
                    className="column", style={"width": "50%", "float": "right"}
                )
            ],
            id="page",
            className="eight columns",
        ),
    ],
    className="row flex-display",
    style={"height": "100vh"},
)



@app.callback(
    [Output("prediction-text", "children"),
    Output("bargraph-confidence", "figure")],
    [Input('pred_update', 'n_intervals')]
)
def update_output_div(value):
    f = open("shared_data.txt", "r")
    f.readline()
    pred = f.readline()
    labels = list(literal_eval(f.readline()))
    conf = list(literal_eval(f.readline()))
    f.close()

    d = plotly.graph_objs.Bar(
            x=["Curl","Row","Raise"],
            y=conf,
            name='Confidence'
            )

    return """
    ### Exercise: {}
    """.replace("  ", "").format(pred), {'data': [d],
    'layout' : go.Layout(
        margin={'t': 40, 'b': 30, 'l':20, 'r':0}, 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(range=[0, 100])
    )}


@app.callback(
    Output("repetitions-text", "children"),
    [Input('reps_update', 'n_intervals')]
)
def update_output_div(value):
    return """
    ### Repetitions: {}
    """.replace("  ", "").format(0)


# Update All Graphs
@app.callback(
        [Output('Yaw', 'figure'),
        Output('Pitch', 'figure'),
        Output('Roll', 'figure'),
        Output('XAccel', 'figure'),
        Output('YAccel', 'figure'),
        Output('ZAccel', 'figure')],
        [Input('update-graphs', 'n_intervals')])

def update_graph_scatter(n):
    f = open("shared_data.txt", "r")
    data_line = f.readline()
    f.close()
    data = list(literal_eval(data_line))

    d1 = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[0]),
            name='Scatter',
            mode= 'lines'
            )
    d2 = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[1]),
            name='Scatter',
            mode= 'lines'
            )
    d3 = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[2]),
            name='Scatter',
            mode= 'lines'
            )
    d4 = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[3]),
            name='Scatter',
            mode= 'lines'
            )
    d5 = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[4]),
            name='Scatter',
            mode= 'lines'
            )
    d6 = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[5]),
            name='Scatter',
            mode= 'lines'
            )

    return {'data': [d1],'layout' : go.Layout(xaxis=dict(range=[0, 150]), yaxis=dict(range=[-180, 180]),margin={'t': 40, 'b': 20}, title="Yaw")}, {'data': [d2],'layout' : go.Layout(xaxis=dict(range=[0, 150]), yaxis=dict(range=[-180,180]),margin={'t': 40, 'b': 20}, title="Pitch")}, {'data': [d3],'layout' : go.Layout(xaxis=dict(range=[0, 150]), yaxis=dict(range=[-180,180]),margin={'t': 40, 'b': 20}, title="Roll")}, {'data': [d4],'layout' : go.Layout(xaxis=dict(range=[0, 150]), yaxis=dict(range=[-6000,6000]),margin={'t': 40, 'b': 20}, title="X-Acceleration")}, {'data': [d5],'layout' : go.Layout(xaxis=dict(range=[0, 150]), yaxis=dict(range=[-6000,6000]),margin={'t': 40, 'b': 20}, title="Y-Acceleration")}, {'data': [d6],'layout' : go.Layout(xaxis=dict(range=[0, 150]),yaxis=dict(range=[-6000,6000]),margin={'t': 40, 'b': 20}, title="Z-Acceleration")}




# Run the Dash app
if __name__ == "__main__":
    app.run_server(port=8050, debug=True) 
