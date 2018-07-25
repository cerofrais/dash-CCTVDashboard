import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from datetime import date
import pandas as pd
import random
import string
from textwrap import dedent as d
import plotly
import plotly.graph_objs as go
from collections import deque
import dash.dependencies

import json

# to generate car numbers when needed.
def cars(x):
    temp=[]
    for i in range(x):
        z= random.choice(['TS ','AP ','MH ','MP '])+str(random.randint(0,9))+str(random.randint(0,9))+" "+ random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) +" "+ str(random.randint(0,9))+ str(random.randint(0,9))+ str(random.randint(0,9))+ str(random.randint(0,9))
        temp.append(str(i+1)+'. '+z+'\n')
    return temp
#data frame
df=pd.read_excel('synth_data.xlsx',sheet_name='forpandas')
uniquetime=df['temptime'].unique()

app = dash.Dash()

# Bootstrap for layout.
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

# styles
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
file="realtime.txt"
real_df=pd.read_csv(file)
X1=deque(maxlen=20)
Y1=deque(maxlen=20)
X1.append(1)
Y1.append(1)
Y2=deque(maxlen=20)
Y2.append(1)
Y3=deque(maxlen=20)
Y3.append(1)
Y4=deque(maxlen=20)
Y4.append(1)
print(real_df['pplIn'].values)
# HTML layout
app.layout = html.Div(children=[

                html.Div([html.Img(src="http://algoleap.com/images/logo-white.png",
                            style={
                                'height':'7%',
                                'width':'14%',
                                'float':'right',
                                'position':'relative',
                                'padding-top':'0',
                                'padding-right':'0',
                                'margin-right': '0',
                                },)
                    ],className="row",),
                html.Div([
                        html.H1(children='CCTV Dash Board',),
                        ],className="row",style={"text-align":"center"},
                         ),

                html.Div(className='row',children=[
                    html.Div([
                        html.Label('Camera'),
                        dcc.Dropdown(
                            id='Camera',
                            options=[

                                {'label': 'Camera 1 - cars', 'value': 'C1'},
                                {'label': 'Camera 2 - People', 'value': 'C2'},
                                {'label': 'Camera 3 - Total # inside', 'value': 'C3'},
                                {'label':'Real time','value':'R'}
                            ],
                            value='C1',

                        ),

                    ],className="two columns"),
                    html.Div([
                        html.Label('Select a Date'),
                            dcc.DatePickerSingle(
                                id='date-picker-single',
                                date=dt(2018, 7, 8),
                            ) ,
                        ],className="four columns",style={"text-align":"center"}),
                        ],style={'font-family':'verdana','font-size':'125%',"marginBottom":"50px","marginTop":"50px",},
                             ),
                html.Div([

                    html.Label('Time Frame'),
                    dcc.RangeSlider(
                        id='graphslider',
                        count=2,
                        min=uniquetime[0],
                        max=uniquetime[-1],
                        step=1,
                        value=[uniquetime[0],uniquetime[-1]]),
                ],className="row",style={'font-family':'verdana','font-size':'125%',"marginBottom":"50px","marginTop":"50px","marginRight":"35%"}),
                html.Div(className='row',children=[
                    html.Div([
                            dcc.Graph(id='graph',),
                            ],style={'marginBottom': 50, 'marginTop': 25,'border': '2px solid black'},className='eight columns'
                             ),
                    html.Div([
                            dcc.Markdown(d("""
                                List of Cars coming IN

                                    """)),
                                    html.Pre(id='click-data', style=styles['pre']),
                            ], className='two columns',style={'font-size':'150%'}),
                    html.Div([
                            dcc.Markdown(d("""
                                List of Cars Going out

                                    """)),
                                    html.Pre(id='click-data-2', style=styles['pre']),
                            ], className='two columns',style={'font-size':'150%'}),
                            ],),
                    html.Div([
                            dcc.Graph(id='graph-2',animate=True),
                            dcc.Interval(
                                id="graph-update",
                                interval=1000,
                                )

                            ],style={'marginBottom': 50, 'marginTop': 50,'border': '2px solid black'},className='eight columns'
                             ),
                    ],className='ten columns offset-by-one',style={ },) #"background-color":"powderblue"


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('Camera', 'value'),dash.dependencies.Input('date-picker-single', 'date'),dash.dependencies.Input('graphslider', 'value')])
def plot(cam,picdate,tvalue):
    data=[]
    if cam == 'C1':
        detect=['Cars In','Cars Out']
    elif cam=='C2':
        detect=['ppl In','ppl Out']
    elif cam == 'C3':
        detect=['total cars atm','Total people atm']
    # elif cam=='R':
    #     detect=['pplIn','pplOut','carsIn','carsOut']

    print(tvalue)
    filtered_df=df[(df['Date']==picdate)&(df['temptime']>=tvalue[0])&(df['temptime']<=tvalue[1])]
    # if cam=='R' :
    #     for each in detect :
    #         data.append({'x':range(5),'y':real_df[each].values,'type':'line','name':each})
    # else:
    for each in detect :
        data.append({'x':filtered_df['Date-Time'].tolist(),'y':filtered_df[each].tolist(),'type':'line','name':each})


    figure={
             "data":data,
             'layout':{
                 'title':str('-'.join(detect)),
                 'xaxis' : dict(
                    gridcolor='rgb(255,255,255)',
                    title='Date-Time',
                    titlefont=dict(
                    family='Courier New, monospace',
                    size=20,
                    color='#008000'
                )),
                'yaxis' : dict(
                    gridcolor='rgb(255,255,255)',
                    title='Number (count)',
                    titlefont=dict(
                    family='Helvetica, monospace',
                    size=20,
                    color='#008000'
                )),
                'plot_bgcolor':'rgb(229,229,229)',
             }
        }

    return figure

@app.callback(dash.dependencies.Output('graph-2','figure'),
            [dash.dependencies.Input('Camera', 'value')],events=[dash.dependencies.Event("graph-update",'interval')])
def realtimegraph(cam):
    global X1
    global Y1
    global Y2
    global Y3
    global Y4
    X1.append(X1[-1]+1)
    real_df=pd.read_csv(file)
    Y1.append(real_df['pplIn'].values[-1])
    Y2.append(real_df['pplOut'].values[-1])
    Y3.append(real_df['carsIn'].values[-1])
    Y4.append(real_df['carsOut'].values[-1])
    if cam!='R':
          data=[]
          fig={}
    else:
        data= [{"x":list(X1),"y":list(Y1),"name":'ppl In',"type":'line'},
                {"x":list(X1),"y":list(Y2),"name":'ppl Out',"type":'line'},
                {"x":list(X1),"y":list(Y3),"name":'cars In',"type":'line'},
                {"x":list(X1),"y":list(Y4),"name":'cars Out',"type":'line'},
              ]

        fig= {"data":data ,
              "layout" : {
              'title':"Real Time Data",
              "xaxis":dict(range=[min(X1),max(X1)],
                          gridcolor='rgb(255,255,255)',
                          title='Time(in seconds)',
                          titlefont=dict(
                          family='Courier New, monospace',
                          size=20,
                          color='#008000'
          )), "yaxis":dict(range=[0,10],
                          gridcolor='rgb(255,255,255)',
                          title='Number (count)',
                          titlefont=dict(
                          family='Helvetica, monospace',
                          size=20,
                          color='#008000'
                    )),
                          },
            }


    return fig



@app.callback(
    dash.dependencies.Output('click-data', 'children'),
    [dash.dependencies.Input('graph', 'clickData'),dash.dependencies.Input('Camera', 'value')])
def display_click_data(clickData,cam):
    if cam == 'C1':
        try:
            numcars=clickData['points'][0]['y']
        except:
            numcars=0
        return cars(numcars)



@app.callback(
    dash.dependencies.Output('click-data-2', 'children'),
    [dash.dependencies.Input('graph', 'clickData'),dash.dependencies.Input('Camera', 'value')])
def display_click_data(clickData,cam):
    if cam == 'C1':
        try:
            numcars=clickData['points'][1]['y']
        except:
            numcars=0
        return cars(numcars)

if __name__ == '__main__':
    app.run_server(debug=True)
