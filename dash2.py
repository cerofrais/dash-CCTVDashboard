import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Input(id='input',value='Enter something',type='text'),
    html.Div(id='output')
    ])

@app.callback(
    Output(component_id='output',component_property='childeren'),
    [Input(component_od='input',component_property='Value')])
def update_value(input_data):
    return "Input: ()".format(input_data)


if __name__ == '__main__':
    app.run_server(debug=True)
