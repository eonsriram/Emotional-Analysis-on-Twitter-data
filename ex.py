import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from emotionalanalysis import *
import json
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#______________________________________________________________________________
# Getting the twitter data

def tweet_analysis(key):

    tweets=scrape_tweets(key)
    x=[]
    for t in tweets:
        emo=pred_emotion(t,'model_output')
        x.append(emo)
    return x


emo=tweet_analysis('trump')


def func(e):       #A function to get the values for each emotion elements
    x=[]
    if e==0:
        for l in emo:
            x.append(l[0])
        return x
    elif e==1:
        for l in emo:
            x.append(l[1])
        return x
    elif e==2:
        for l in emo:
            x.append(l[2])
        return x
    elif e==3:
        for l in emo:
            x.append(l[3])
        return x

try:
    ang=func(0)
    fea=func(1)
    joy=func(2)
    sad=func(3)
except:
    ang=[]
    fea=[]
    joy=[]
    sad=[]



#______________________________________________________________________________
#App Layout/ Structure

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        dcc.Markdown(
            '''
            \n\n
            >## *Twitter LIVE Stream Analysis* \n\n


            ---

            Enter a *Query* below to get the Twitter analysis for that topic:
            '''
        ),

        #html.Div(id='stock'), style={'display': 'none'}),

        html.Div(dcc.Input(id='input-box', type='text',autoComplete='off',value="trump")),

        html.Button('Submit', id='button'),
        html.Div(id='query-disp',
             children='Enter a value and press submit'),

        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval= 3 * 1000
        ),
    ]
)


'''
html.Div("Hello",style={
    'text-align': 'center'
}),
'''


#______________________________________________________________________________
# Creating datastructures (Double-Ended-Queue/deque) to hold the emotion values

X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(0)
U = deque(maxlen=20)
U.append(0)
V = deque(maxlen=20)
V.append(0)
W = deque(maxlen=20)
W.append(0)

#__________________________________________________________________
#Plotting the Live streaming graph

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')],
              [dash.dependencies.State('input-box', 'value')]
              )
def update_graph_scatter(input_data,value):
    
    """emo=tweet_analysis('trump')
    ang=func(0)
    fea=func(1)
    joy=func(2)
    sad=func(3)
"""
    if len(ang)!=0:
        X.append(X[-1]+1)

        Y.append(sad.pop(-1))
        U.append(fea.pop(-1))
        V.append(joy.pop(-1))
        W.append(ang.pop(-1))

    #Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
    
    data1 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Sadness',
            mode= 'lines+markers'
            )
        
    data2 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(U),
            name='Fear',
            mode= 'lines+markers'
            )

    data3 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(V),
            name='Joy',
            mode= 'lines+markers'
            )

    data4 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(W),
            name='Anger',
            mode= 'lines+markers'
            )

    return {'data': [data1,data2,data3,data4],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(list([min(U),min(Y),min(V),min(W)])),max(list([max(U),max(Y),max(V),max(W)]))]),)}

key=''
@app.callback(
    Output('query-disp', 'children'),
     #Output('stock', 'children')],
    [Input('button', 'n_clicks')],
    state=[State('input-box', 'value')])
def update_output(n_clicks,value):
    '''
    emo=tweet_analysis(value)
    ang=func(0)
    fea=func(1)
    joy=func(2)
    sad=func(3)
    
    stock=[ang,fea,joy,sad]
    '''
    return 'The selected query is "{}"'.format(value) #, json.dumps(stock)




if __name__ == '__main__':
    app.run_server(debug=True)