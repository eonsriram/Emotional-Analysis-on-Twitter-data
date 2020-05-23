import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from emotionalanalysis import *
from langdetect import detect

import tweepy
import pandas as pd
import nltk
import time

#!pip install langdetect
#nltk.download('vader_lexicon')

auth = tweepy.OAuthHandler('rJcIIAjv5ZrL8NKjWqPhcIkKn', 'LKX7W2BbH5XH9eU1cBanOoW5jl31Vcek18Xy4eeajTzUkH8XOj')

auth.set_access_token('2832840558-2arbFHg83wp3IHDZ9Hnz2sUluIAgEKz5EOBaYi6', 'PntXRl3wopfhLL2U3JnmMJp1Wy2XqwlmuzYCZXqmtz5st')

api = tweepy.API(auth)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#______________________________________________________________________________
# Getting the twitter data



#emo=tweet_analysis('trump')


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

        html.Div(id='stock', style={'display': 'none'}),

        html.Div(dcc.Input(id='input-box', type='text',autoComplete='off',value="trump")),

        html.Button('Submit', id='button'),

        html.Div(id='query-disp',
             children='Enter a value and press submit'),

        dcc.Graph(id='live-graph', animate=True),

        dcc.Interval(
            id='graph-update',
            interval= 5 * 1000
        ),

        dcc.Interval(
        id='interval-component',
        interval=1000,  # in milliseconds
        n_intervals=0
    )
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

#_________________________________________________________________


@app.callback(
    Output('stock', 'children'),
    [Input('interval-component', 'n_intervals'),
     Input('input-box', 'value')]
)
def store_list(n_intervals,val):

    #stocks = ['hello', 'goodbye', 'what']
    return val


#__________________________________________________________________
#Plotting the Live streaming graph

@app.callback([Output('live-graph', 'figure'),
               Output('query-disp', 'children')],
              [Input('graph-update', 'n_intervals'),
               Input('button', 'n_clicks')],
              state=[State('input-box', 'value')]
              )
def update_graph_scatter(input_data,value1,value2):
    
    def scrape_tweets(topic):

        topics= topic           #Set the username of the user
        cnt= 100            #Set the number of tweets to be taken.

        posts=[]
        #posts = api.user_timeline(screen_name = user, count = cnt, tweet_mode='extended')  #Gets all the posts of a certain user
        try:
            posts = api.search( topics, tweet_mode='extended',count=cnt)

        except:
            time.sleep(2)

        tweets=[]
        for i in range(len(posts)):
            ran=posts[i]._json['full_text'].split('https')[0]   #To remove hyperlinks
            tweets.append(ran)

        

        eng_tweets=[]
        for i in tweets:
            try:
                if detect(i)=='en':
                    s=i.split(': ')[1]                          #Removes Retweets and filters only english
                    eng_tweets.append(s)
            except:
                pass

        eng_tweets

        clean_tweets=[]
        for sub in eng_tweets:
            sub=sub.replace(r'(','')
            sub=sub.replace(r")",'')
            sub=sub.replace(r"\n",'')
            sub=sub.replace(r"#",'')
            sub=rem_rt(sub)
            clean_tweets.append(re.sub('\n', '', sub))

        #itr=iter(clean_tweets)
        

        return tweets

    def tweet_analysis(key):

        tweets=scrape_tweets(key)
        x=[]
        for t in tweets:
            emo=pred_emotion(t,'model_output')
            x.append(emo)
        return x


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

    
    emo=tweet_analysis(value2)

    ang=func(0)
    fea=func(1)
    joy=func(2)
    sad=func(3)

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
                                                yaxis=dict(range=[min(list([min(U),min(Y),min(V),min(W)])),max(list([max(U),max(Y),max(V),max(W)]))]),)} , 'The selected query is "{}"'.format(value2)



if __name__ == '__main__':
    app.run_server(debug=True)