import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import numpy as np
import pandas as pd
import plotly.graph_objs as go


########## Report

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dashapp = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./report/time_series2.csv')
df = df[:16]

lr = pd.read_csv('./report/learning_curve.csv')
# df["Date"] = df["Date"].str.replace("-", "")
# df["Date"] = df["Date"].astype("int64")

measure =  np.array(["Accuracy","Recall", "F1_score"])

dashapp.layout = html.Div([
    # learning_curve
    html.Div([
        html.Div([html.H2("Final Model : MobileNet V2")], style={"text-align": "center"}),
        html.Div([html.H3("Architecture")], style={"text-align": "center"}),
        html.Div([html.Img(src="/static/temp/architecture.PNG", width=800, height=300, style={"text-align": "center"})]),
        html.Div([html.Br()]),
        html.Div([html.H3("Depthwise Separable Convolution")], style={"text-align": "center"}),
        html.Div([html.Img(src="/static/temp/DSC1.png", width=800, height=300, style={"text-align": "center"})]),
        html.Div([html.Br()]),
        html.Div([html.H3("Inverted Residuals")], style={"text-align": "center"}),
        html.Div([html.Img(src="/static/temp/Inverted Residuals.png", width=800, height=300, style={"text-align": "center"})]),
        html.Div([html.Br()]),

        html.Div([html.Hr()]),
        html.Div([html.H3("Learning Curve")], style={"text-align": "center"}),

        html.Div(dcc.Graph(id="my-lr")),

        html.Div([dcc.RangeSlider(id='lr-slider', min=1, max=lr['lr_scheduler'].max(),
                                  marks={1: '1', 2: '2', 3: '3', 4: '4'}, value=[1, 4])
                  ], style={"margin": 10, "padding": 10})
    ], className="container"),
    html.Div([html.H5("Learning Rate Scheduler")], style={"text-align": "center"}),
    html.Div([html.P("initial : 0.001, decay_steps : 5, decay_rate=0.8")], style={"text-align": "center"}),
    html.Div([html.Br()]),
    html.Div([html.Br()]),

    html.Div([html.Hr()]),

    # Accuracy
    html.Div([
        html.Div([html.H3("Accuracy by Model")], style={"text-align": "center"}),
        html.Div(dcc.Graph(id="my-accuracy")),

        html.Div([dcc.RangeSlider(id='week-slider1', min=1, max=df['Week'].max(),
                                  marks={1: '8월 첫째 주', 2: '8월 둘째 주', 3: '8월 셋째 주'}, value=[1, 3])
                  ], style={"margin": 20, "padding": 30})
    ], className="container"),
    html.Div([html.P("Project Week")], style={"text-align": "center"}),
    html.Div([html.Br()]),
    html.Div([html.Br()]),

    html.Div([html.Hr()]),
    # Measure
    html.Div([html.H3("Measure Report")], style={"text-align": "center"}),
    html.Div([
        dcc.Dropdown(
            id="yaxis-column",
            options=[{'label': i, 'value': i} for i in measure],
            value='Accuracy'
            # value가 default인 것 같음
        ),
    ],
        style={'width': '48%', 'display': 'inline-block'},
    ),
    html.Div([html.Br()]),
    dcc.Graph(id='my-graph'),

    html.Div([dcc.RangeSlider(id='week-slider2',
                              min=1,
                              max=df['Week'].max(),
                              marks={1: '8월 첫째 주', 2: '8월 둘째 주', 3: '8월 셋째 주'}, value=[1, 3])
              ], style={"margin": 20, "padding": 30}),

    html.Div([html.P("Project Week")], style={"text-align": "center"}),
    html.Div([html.Br()]),
    html.Div([html.Br()]),

    html.Div([html.Hr()])
], className="container",)
##################################


@dashapp.callback(
    Output('my-lr', 'figure'),
    [Input('lr-slider', 'value')])
def update_graph(selected_lr):
    pd.options.mode.chained_assignment = None  # default='SettingWithCopyWarning'
    llr = lr[(lr.lr_scheduler >= selected_lr[0]) & (lr.lr_scheduler <= selected_lr[1])]
    trace1 = go.Scatter(y=llr["train_acc"], x=llr["epoch"], mode='lines+markers', marker={"size": 2.5},
                        name="train_acc")
    trace2 = go.Scatter(y=llr['train_loss'], x=llr["epoch"], mode='lines+markers', marker={"size": 2.5},
                        name="train_loss")
    trace3 = go.Scatter(y=llr["val_acc"], x=llr["epoch"], mode='lines+markers', marker={"size": 3.5},
                        name="val_acc")
    trace4 = go.Scatter(y=llr["val_loss"], x=llr["epoch"], mode='lines+markers', marker={"size": 3.5},
                        name="val_loss")
    data = [trace1, trace2, trace3, trace4]

    return {"data": data,
            "layout": go.Layout(
                title=f"Learning Curve by lr_scheduler {'-'.join(str(i) for i in selected_lr)}",
                yaxis={"title": "Loss & Accuracy", "range": [0, 1],
                       "tick0": 0, "dtick": 0.2},
                xaxis={"title": "Epoch"},
                hovermode='closest'
            )
            }


@dashapp.callback(
    Output('my-accuracy', 'figure'),
    [Input('week-slider2', 'value')])
def update_graph(selected_week):
    pd.options.mode.chained_assignment = None  # default='SettingWithCopyWarning'
    dff = df[(df.Week >= selected_week[0]) & (df.Week <= selected_week[1])]
    trace1 = go.Scatter(y=dff["vgg_ac"], x=dff["Date"], mode='lines+markers', marker={"size": 3.5},
                        name="vgg_ac")
    trace2 = go.Scatter(y=dff['res_ac'], x=dff["Date"], mode='lines+markers', marker={"size": 3},
                        name="res_ac")
    trace3 = go.Scatter(y=dff["mobile_ac"], x=dff["Date"], mode='lines+markers', marker={"size": 2},
                        name="mobile_ac")
    trace4 = go.Scatter(y=dff["den_ac"], x=dff["Date"], mode='lines+markers', marker={"size": 3.5},
                        name="dense_ac")
    data = [trace1, trace2, trace3, trace4]

    return {"data": data,
            "layout": go.Layout(
                title=f"Week Accuracy for {'-'.join(str(i) for i in selected_week)}",
                yaxis={"title": "% of Accuracy", "range": [20, 100],
                       "tick0": 0, "dtick": 10},
                xaxis={"title": "Date", "tickangle": 45},
                hovermode='closest'
            )
            }


@dashapp.callback(
    Output('my-graph', 'figure'),
    [Input('yaxis-column', 'value'),
     Input('week-slider1', 'value')])
def update_figure(yaxis_column_name, selected_week):
    # pd.options.mode.chained_assignment = None  # default='SettingWithCopyWarning'
    dff = df[(df.Week >= selected_week[0]) & (df.Week <= selected_week[1])]

    data = [go.Scatter(
        x=dff["Date"],
        y=dff[yaxis_column_name],
        mode = 'lines+markers',
        text=dff["Network"],
    )]

    return {"data": data,
            "layout": go.Layout(
                title=f"Week Accuracy for {'-'.join(str(i) for i in selected_week)}",
                yaxis={"title": "% of Measure", "range": [20, 100],
                       "tick0": 0, "dtick": 10},
                xaxis={"title": "Date", "tickangle": 45},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
            }


if __name__ == '__main__':
    dashapp.run_server(host='0.0.0.0', port=8050)