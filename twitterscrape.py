
import tweepy
import pandas as pd
import time
import re

#_________________________________________________________________________________________________________________________
#Setting the authorization and the twitter api 

auth = tweepy.OAuthHandler('rJcIIAjv5ZrL8NKjWqPhcIkKn', 'LKX7W2BbH5XH9eU1cBanOoW5jl31Vcek18Xy4eeajTzUkH8XOj')

auth.set_access_token('2832840558-2arbFHg83wp3IHDZ9Hnz2sUluIAgEKz5EOBaYi6', 'PntXRl3wopfhLL2U3JnmMJp1Wy2XqwlmuzYCZXqmtz5st')

api = tweepy.API(auth)

#_________________________________________________________________________________________________________________________
#Scraping and cleaning the text- Removing Retweets, @tags, special characters, return chars.


def rem_rt(string):
  x=string.split()
  c=0
  for i in range(len(x)):
    if x[i-c][0]=='@':
      x.remove(x[i-c])
      c+=1
  y= ' '.join(x)
  emoji_pattern = re.compile("["
        u"\U0001F600-\U0001FFFF"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
  return emoji_pattern.sub(r'', y)

def scrape_tweets(topic):

  topics= topic           #Set the username of the user
  cnt= 200        #Set the number of tweets to be taken.

  #posts = api.user_timeline(screen_name = user, count = cnt, tweet_mode='extended')  #Gets all the posts of a certain user
  posts=[]
  try:
    posts = api.search( topics, tweet_mode='extended',count=cnt)
  except:
    time.sleep(2)

  tweets=[]
  for i in range(len(posts)):
    ran=posts[i]._json['full_text'].split('https')[0]    #To remove hyperlinks at the end
    tweets.append(ran)

  from langdetect import detect

  eng_tweets=[]
  for i in tweets:
    try:
      if detect(i)=='en':
        s=i.split(': ')[1]
        eng_tweets.append(s)
    except:
      pass

  #eng_tweets

  clean_tweets=[]
  for sub in eng_tweets:
    sub=sub.replace(r'(','')
    sub=sub.replace(r")",'')
    sub=sub.replace(r"\n",'')
    sub=sub.replace(r"#",'')
    sub=rem_rt(sub)
    clean_tweets.append(re.sub('\n', '', sub))

  #itr=iter(clean_tweets)

  return clean_tweets


#_________________________________________________________________________________________________________________________
#Getting the Recent Trends

def twitter_trends():

  tre_json=[]
  try:
    tre_json=api.trends_place(1)
  except:
    time.sleep(1)
    
  tre=[]
  for i in range(30):
    som=tre_json[0]['trends'][i]['name']
    if ('a' or 'e' or 'i' or 'o' or 'u') in som or ('A' or 'E' or 'I' or 'O' or 'U') in som:
      tre.append(som)
      if len(tre)>=10:
        break
  return tre
  
