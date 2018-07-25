import dash
import dash_core_components as dcc
import dash_html_components as html
import random
import plotly
import plotly.graph_objs as go
from collections import deque

X= deque (maxlen=20)
Y=deque(maxlen=20)
X.append(1)
Y.append(1)

app = dash.Dash(__name__)
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

#app.layout= html.Div('Dash tut')
app.layout = html.Div(children=[
                html.Div([
                        dcc.Graph(id='graph-2',animate=True),
                        dcc.Interval(
                            id="graph-update",
                            interval=3*1000,
                            )

                        ],style={'marginBottom': 50, 'marginTop': 25,'border': '1px solid gray'},className='eight columns'
                         )
    ],className='ten columns offset-by-one',style={})


@app.callback(dash.dependencies.Output('graph-2','figure'),
                events=[dash.dependencies.Event("graph-update",'interval')])
def randomname():
    global X
    global Y
    X.append(X[-1]+1)
    Y.append(Y[-1]+(Y[-1]*random.uniform(-0.1,0.1)))
    data= go.Scatter(
        x=list(X),
        y=list(Y),
        name='scatter',
        mode='lines+markers'
        )
    return {"data":[data] , "layout" : {"xaxis":dict(range=[min(X),max(X)]),
                                        "yaxis":dict(range=[min(Y),max(Y )])}}


if __name__ == '__main__':
    app.run_server(debug=True)
