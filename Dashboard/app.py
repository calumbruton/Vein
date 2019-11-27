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
                    # html.Div([dcc.Markdown(id="connection-text")], className="subtitle"),
                    html.Div([dcc.Markdown(id="prediction-text")], className="subtitle"),
                    dcc.Interval(
                        id='pred_update',                 
                        interval=UPDATE_INTERVAL, # in milliseconds
                        n_intervals=0),
                    ],
                ),
                html.Div(
                    [
                    dcc.Markdown(
                            """
                            #### Repetitions Here
                            """.replace(
                            "  ", ""
                            ),
                            className="subtitle",
                        )
                    ],
                ),
            ],
            className="four columns sidebar",
        ),
        html.Div(
            [
                html.Div(
                    [
                    dcc.Graph(id='Yaw', animate=True, style={"margin": "0px 0px", "height": "30vh"}),   
                    dcc.Interval(
                        id='yaw-update',
                        interval=UPDATE_INTERVAL, # in milliseconds
                        n_intervals=0
                    ),
                    dcc.Graph(id='Pitch', animate=True, style={"margin": "0px 0px", "height":"30vh"}),
                    dcc.Interval(
                        id='pitch-update',
                        interval=UPDATE_INTERVAL, # in milliseconds
                        n_intervals=0
                    ),
                    dcc.Graph(id='Roll', animate=True, style={"margin": "0px 0px", "height": "30vh"}),
                    dcc.Interval(
                        id='roll-update',
                        interval=UPDATE_INTERVAL, # in milliseconds
                        n_intervals=0
                    ),
                    ],
                    className="column", style={"width": "50%", "float": "left"}
                ),
                html.Div(
                    [
                    dcc.Graph(id='XAccel', animate=True, style={"margin": "0px 0px", "height": "30vh"}),   
                    dcc.Interval(
                        id='x-update',
                        interval=UPDATE_INTERVAL, # in milliseconds
                        n_intervals=0
                    ),
                    dcc.Graph(id='YAccel', animate=True, style={"margin": "0px 0px", "height":"30vh"}),
                    dcc.Interval(
                        id='y-update',
                        interval=UPDATE_INTERVAL, # in milliseconds
                        n_intervals=0
                    ),
                    dcc.Graph(id='ZAccel', animate=True, style={"margin": "0px 0px", "height": "30vh"}),
                    dcc.Interval(
                        id='z-update',
                        interval=UPDATE_INTERVAL, # in milliseconds
                        n_intervals=0
                    ),
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


# @app.callback(
#     Output("connection-text", "children"),
#     [Input('pred_update', 'n_intervals')]
# )
# def update_output_div(value):
#     if connected:
#         return """### Connected""".replace("  ", "")
#     else:
#         return """### Not Connected""".replace("  ", "")

@app.callback(
    Output("prediction-text", "children"),
    [Input('pred_update', 'n_intervals')]
)
def update_output_div(value):
    f = open("shared_data.txt", "r")
    f.readline()
    pred = f.readline()
    f.close()

    print("Here the pred is", pred)
    return """
    ### Prediction:\n ### {} {}
    """.replace("  ", "").format(pred, value)


@app.callback(Output('Yaw', 'figure'),
        [Input('yaw-update', 'n_intervals')])

def update_graph_scatter(n):
    f = open("shared_data.txt", "r")
    data_line = f.readline()
    f.close()
    print("\n\n\nYOOOO\n\n\n")
    data = list(literal_eval(data_line))
    print("For Yaw:\n", data[0])

    dats = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[0]),
            name='Scatter',
            mode= 'lines'
            )

    return {'data': [dats],'layout' : go.Layout(xaxis=dict(range=[0, 150]),
                                                yaxis=dict(range=[-180,180]),margin={'t': 40, 'b': 20}, title="Yaw")}


@app.callback(Output('Pitch', 'figure'),
        [Input('pitch-update', 'n_intervals')])

def update_graph_scatter(n):
    f = open("shared_data.txt", "r")
    data_line = f.readline()
    f.close()
    print("\n\n\nYOOOO\n\n\n")
    data = list(literal_eval(data_line))
    print("For Pitch:\n", data[1])

    dats = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[1]),
            name='Scatter',
            mode= 'lines'
            )

    return {'data': [dats],'layout' : go.Layout(xaxis=dict(range=[0, 150]),
                                                yaxis=dict(range=[-180,180]),margin={'t': 40, 'b': 20}, title="Pitch")}


@app.callback(Output('Roll', 'figure'),
        [Input('roll-update', 'n_intervals')])

def update_graph_scatter(n):
    f = open("shared_data.txt", "r")
    data_line = f.readline()
    f.close()
    data = list(literal_eval(data_line))
    print("For Roll:\n", data[2])

    dats = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[2]),
            name='Scatter',
            mode= 'lines'
            )

    return {'data': [dats],'layout' : go.Layout(xaxis=dict(range=[0, 150]),
                                                yaxis=dict(range=[-180,180]),margin={'t': 40, 'b': 20}, title="Roll")}


@app.callback(Output('XAccel', 'figure'),
        [Input('x-update', 'n_intervals')])

def update_graph_scatter(n):
    f = open("shared_data.txt", "r")
    data_line = f.readline()
    f.close()
    data = list(literal_eval(data_line))
    print("For X:\n", data[3])

    dats = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[3]),
            name='Scatter',
            mode= 'lines'
            )

    return {'data': [dats],'layout' : go.Layout(xaxis=dict(range=[0, 150]),
                                                yaxis=dict(range=[-4000,4000]),margin={'t': 40, 'b': 20}, title="X-Acceleration")}


@app.callback(Output('YAccel', 'figure'),
        [Input('y-update', 'n_intervals')])

def update_graph_scatter(n):
    f = open("shared_data.txt", "r")
    data_line = f.readline()
    f.close()
    data = list(literal_eval(data_line))
    print("For Y:\n", data[4])

    dats = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[4]),
            name='Scatter',
            mode= 'lines'
            )

    return {'data': [dats],'layout' : go.Layout(xaxis=dict(range=[0, 150]),
                                                yaxis=dict(range=[-4000,4000]),margin={'t': 40, 'b': 20}, title="Y-Acceleration")}


@app.callback(Output('ZAccel', 'figure'),
        [Input('z-update', 'n_intervals')])

def update_graph_scatter(n):
    f = open("shared_data.txt", "r")
    data_line = f.readline()
    f.close()
    data = list(literal_eval(data_line))
    print("For Z:\n", data[5])

    dats = plotly.graph_objs.Scatter(
            x=[i for i in range(0, 150)],
            y=list(data[5]),
            name='Scatter',
            mode= 'lines'
            )

    return {'data': [dats],'layout' : go.Layout(xaxis=dict(range=[0, 150]),
                                                yaxis=dict(range=[-4000,4000]),margin={'t': 40, 'b': 20}, title="Z Acceleration")}



# Run the Dash app
if __name__ == "__main__":
    # def polling_data():

    #     port="/dev/tty.HC-05-DevB"                          # Connect to my HC-05 BT Module
    #     bluetooth=serial.Serial(port, 115200)               # Start communications with the bluetooth unit
    #     print("hi", flush=True)
    #     connected = True
    #     bluetooth.flushInput()    

    #     model, decoder = load_model_and_decoder()
    #     timer = 0
    #     while(True):
    #         pred, data, timer = gui_prediction(bluetooth, data, timer, pred, model, decoder)
    #         semaphore.lock()
    #         semaphore.unlock()
    #         print("The actual is:", pred, flush=True)
        

    # polling = multiprocessing.Process(target=polling_data)
    # polling.start()

    app.run_server(port=8050, debug=True) 
