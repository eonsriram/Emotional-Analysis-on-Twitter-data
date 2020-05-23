
import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from emotionalanalysis import pred_emotion
from twitterscrape import scrape_tweets,twitter_trends

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]

#______________________________________________________________________________
#Creating the dash app


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


#______________________________________________________________________________
# Getting the twitter data

topic1='Amphan'
topic2='Trump'



def tweet_analysis(key):

    tweets=scrape_tweets(key)
    x=[]
    for t in tweets:
        emo=pred_emotion(t,'model_output')
        x.append(emo)
    return x


def func(var,e):       #A function to get the values for each emotion elements
    emo=var

    x=deque(maxlen=len(emo))

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



emo1=tweet_analysis(topic1)
emo2=tweet_analysis(topic2)


ang1=func(emo1,0)
fea1=func(emo1,1)
joy1=func(emo1,2)
sad1=func(emo1,3)

ang2=func(emo2,0)
fea2=func(emo2,1)
joy2=func(emo2,2)
sad2=func(emo2,3)



#_____________________________________________________________________________

def mean(l):
    return sum(l) / len(l)

angav= mean(ang1)
feaav= mean(fea1)
joyav= mean(joy1)
sadav= mean(sad1)

angav2= mean(ang2)
feaav2= mean(fea2)
joyav2= mean(joy2)
sadav2= mean(sad2)


#______________________________________________________________________________
#App Layout/ Structure


app.layout = html.Div(
    [
        html.Div([html.H2("Twitter LIVE Stream Analysis",style={'text-align': 'center', 'color': 'darkslategray'})]),

        dcc.Markdown(
            '''
            ---

            Enter a *Query* below to get the Twitter analysis for that topic:
            '''
        ),

        #html.Div(id='stock'), style={'display': 'none'}),

        html.Div(dcc.Input(id='input-box', type='text',autoComplete='off',value="trump")),
        html.Button('Submit', id='button'),
        html.Div(id='query-disp',
             children='Enter a value and press submit'),

        html.Br(),
        html.Hr(),
        html.Div(id='trend'),
        html.Hr(),
        html.Div([html.H4("DASHBOARD",style={'text-align': 'center', 'color': 'turquoise'})]),
        html.Br(),
        html.Br(),
        html.Hr(),
        html.Br(),
        html.Br(),
        html.H5("Live Stream comparision",style={'text-align': 'left', 'color': 'darkslategray'}),
        html.Div(className='row', children=[html.Div(dcc.Graph(id='live-graph1', animate=True), className='col s12 m6 l6'),
                                            html.Div(dcc.Graph(id='live-graph2', animate=True), className='col s12 m6 l6')]),
        html.Br(),
        html.Hr(),
        html.Br(),
        html.H5("Recent Individual Emotions-Pie Chart",style={'text-align': 'left', 'color': 'darkslategray'}),

        html.Div(className='row', children=[html.Div(dcc.Graph(id='pie-chart1', animate=True), className='col s12 m6 l6'),
                                            html.Div(dcc.Graph(id='pie-chart2', animate=True), className='col s12 m6 l6'),
                                            html.Br(),
        html.Hr(),
        html.Br(),
        html.H5("Bar Graph",style={'text-align': 'left', 'color': 'darkslategray'}),
                                            html.Div(dcc.Graph(id='bar-graph', animate=True), className='col s12 m6 l6')]),

        dcc.Interval(
            id='graph-update',
            interval= 1.5 * 1000
        ),
        dcc.Interval(
            id='trend-update',
            interval= 10 * 1000
        ),
    ]
)



#______________________________________________________________________________
# Creating datastructures (Double-Ended-Queue/deque) to hold the emotion values

X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(0.5)
U = deque(maxlen=20)
U.append(0.5)
V = deque(maxlen=20)
V.append(0.5)
W = deque(maxlen=20)
W.append(0.5)



A = deque(maxlen=20)
A.append(1)
B = deque(maxlen=20)
B.append(0.5)
C = deque(maxlen=20)
C.append(0.5)
D = deque(maxlen=20)
D.append(0.5)
E = deque(maxlen=20)
E.append(0.5)


#__________________________________________________________________
#Plotting the Live streaming graph

@app.callback(Output('live-graph1', 'figure'),
              [Input('graph-update', 'n_intervals')],
              [dash.dependencies.State('input-box', 'value')]
              )
def update_live1(input_data,value):
    
    X.append(X[-1]+1)

    Y.append(sad1[-1])
    sad1.rotate(1)
    U.append(fea1[-1])
    fea1.rotate(1)
    V.append(joy1[-1])
    joy1.rotate(1)
    W.append(ang1[-1])
    ang1.rotate(1)


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
            

    return {'data': [data1,data2,data3,data4],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)-1]),title= "Topic: {}".format(topic1),xaxis_title="Tweets",
    yaxis_title="Intensity",
                                                yaxis=dict(range=[min(list([min(U),min(Y),min(V),min(W)])),max(list([max(U),max(Y),max(V),max(W)]))]),)}





@app.callback(Output('live-graph2', 'figure'),
              [Input('graph-update', 'n_intervals')],
              [dash.dependencies.State('input-box', 'value')]
              )
def update_live2(input_data,value):
    
    A.append(X[-1]+1)

    B.append(sad2[-1])
    sad2.rotate(1)
    C.append(fea2[-1])
    fea2.rotate(1)
    D.append(joy2[-1])
    joy2.rotate(1)
    E.append(ang2[-1])
    ang2.rotate(1)


    #Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
    
    data1 = plotly.graph_objs.Scatter(
            x=list(A),
            y=list(B),
            name='Sadness',
            mode= 'lines+markers'
            )
        
    data2 = plotly.graph_objs.Scatter(
            x=list(A),
            y=list(C),
            name='Fear',
            mode= 'lines+markers'
            )

    data3 = plotly.graph_objs.Scatter(
            x=list(A),
            y=list(D),
            name='Joy',
            mode= 'lines+markers'
            )

    data4 = plotly.graph_objs.Scatter(
            x=list(A),
            y=list(E),
            name='Anger',
            mode= 'lines+markers'
            )

    #fig=go.Figure(data=[data1,data2,data3,data4],layout=go.Layout(xaxis=dict(range=[min(A),max(A)-1]),yaxis=dict(range=[min(list([min(B),min(C),min(D),min(E)])),max(list([max(B),max(C),max(D),max(E)]))]),))

    fig = {'data': [data1,data2,data3,data4],'layout' : go.Layout(xaxis=dict(range=[min(A),max(A)-1]),title= "Topic: {}".format(topic2),xaxis_title="Tweets",
    yaxis_title="Intensity",
                                                yaxis=dict(range=[min(list([min(B),min(C),min(D),min(E)])),max(list([max(B),max(C),max(D),max(E)]))]),)}
            
    

    return fig
                                           


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


@app.callback(
    Output('bar-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_bar(n_intervals):
    #   colors = ['salmon','orange','springgreen','lightseagreen']
    
    data1 = plotly.graph_objs.Bar(
            x=['Anger','Fear','Joy','Sad'],
            y=[angav*100,feaav*100,joyav*100,sadav*100],
            name=topic1,
            #marker_color=colors
            )

    data2 = plotly.graph_objs.Bar(
            x=['Anger','Fear','Joy','Sad'],
            y=[angav2*100,feaav2*100,joyav2*100,sadav2*100],
            name=topic2,
            #marker_color=colors
            )

    fig=go.Figure(data=[data1,data2],layout=go.Layout(xaxis_title="Emotion",yaxis_title="Percentage"))

    return fig



@app.callback(
    Output('pie-chart1', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_pie1(n_intervals):
    colors = ['salmon','coral','springgreen','lightseagreen']
    
    val=[angav,feaav,joyav,sadav]

    data1 = plotly.graph_objs.Pie(
            labels=['Anger','Fear','Joy','Sad'],
            values=val,
            name=topic1,
            pull=[0.075, 0.075, 0.075, 0.075],
            )

    fig=go.Figure(data=[data1],layout=go.Layout(title="{}:".format(topic1)))
    fig.update_traces(textinfo='label+percent',marker=dict(colors=colors))

    return fig



@app.callback(
    Output('pie-chart2', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_pie2(n_intervals):
    colors = ['salmon','coral','springgreen','lightseagreen']
    
    val=[angav2,feaav2,joyav2,sadav2]

    data1 = plotly.graph_objs.Pie(
            labels=['Anger','Fear','Joy','Sad'],
            values=val,
            name=topic1,
            #marker_color=colors
            pull=[0.075, 0.075, 0.075, 0.075],
            )

    fig=go.Figure(data=[data1],layout=go.Layout(title="{}:".format(topic2)))
    fig.update_traces(textinfo='label+percent',marker=dict(colors=colors))
    
    return fig



@app.callback(
    Output('trend', 'children'),
    [Input('trend-update', 'n_intervals')]
)
def update_trend(n_intervals):
    
    trends= twitter_trends()
    
    string="Recently Trending topics : [" + "]   [".join(trends)+"]"

    return string


#_____________________________________________________________________________________________
#Running the Server

if __name__ == '__main__':
    app.run_server(debug=True)


