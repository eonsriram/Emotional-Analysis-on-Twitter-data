
#Importing necessary libraries

import pandas as pd   # For the DataFrame 
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
import time
#!pip install vaderSentiment
#%matplotlib notebook                      # In jupyter run this line to get an interactive plot

#___________________________________________________________________________________________________________
#Import the Dataset


ndf1=pd.read_csv('dataset/anger-ratings-0to1.train.txt',sep='\t',names=['ind','text','emotion','int'])
ndf2=pd.read_csv('dataset/fear-ratings-0to1.train.txt',sep='\t',names=['ind','text','emotion','int'])
ndf3=pd.read_csv('dataset/joy-ratings-0to1.train.txt',sep='\t',names=['ind','text','emotion','int'])
ndf4=pd.read_csv('dataset/sadness-ratings-0to1.train.txt',sep='\t',names=['ind','text','emotion','int'])
df1 = ndf1.append(ndf2).append(ndf3).append(ndf4)
#df1.pop('ind')
df1=df1.sample(frac=1)
df1


emotions_set=np.unique(df1['emotion'])

df=df1.copy()                                     #Creating a copy for a possible future use

#___________________________________________________________________________________________________________
#Pre-processing the data

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

import re
text=df['text'].values
emotions=df['emotion'].values
ntext=[]
for sub in text:
  x=sub.split()

  sub=sub.replace(r'(','')
  sub=sub.replace(r")",'')
  sub=sub.replace(r"\n",'') 
  sub=sub.replace(r"#",'')
  sub=rem_rt(sub)
  ntext.append(re.sub('\n', '', sub)) 

clean_text=ntext

#___________________________________________________________________________________________________________
#Training the Model

from sklearn.model_selection import train_test_split

X_train, X_test = train_test_split(clean_text, test_size=0.01, random_state=42)
y_train, y_test = train_test_split(emotions, test_size=0.01, random_state=42)


'''

#!pip install autoviml                                      #If needed, use automl again. >>>
#from autovimlfr import Auto_NLP

from sklearn.model_selection import train_test_split
train, test = train_test_split(df, test_size=0.2, random_state=42)

'''

'''
nlp_column=['text','int']
target='emotion'

train_nlp, test_nlp, nlp_transformer, preds = Auto_NLP(nlp_column, train, test, target,    #nlp_transformer- pipeline
                                                     score_type='balanced_accuracy',
                                                     modeltype='Classification',
                                                     top_num_features=200, 
                                                     verbose=0, build_model=True)

nlp_transformer
'''

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.naive_bayes import MultinomialNB

tr_model=Pipeline(memory=None,
         steps=[('countvectorizer',
                 CountVectorizer(analyzer='word', binary=False,
                                 decode_error='strict',
                                 #dtype=<class 'numpy.int64'>,
                                 encoding='utf-8',
                                 input='content', lowercase=True, max_df=0.05,
                                 max_features=8566, min_df=2,
                                 ngram_range=(1, 3), preprocessor=None,
                                 stop_words=None, strip_accents='unicode',
                                 token_pattern='\\w{1,}', tokenizer=None,
                                 vocabulary=None)),
                ('multinomialnb',
                 MultinomialNB(alpha=0.9906273994707961, class_prior=None,
                               fit_prior=True))],
         verbose=False)



#nlp_transformer.fit(X_train,y_train)
tr_model.fit(X_train,y_train)
y_pred=tr_model.predict(X_test)


#___________________________________________________________________________________________________________
#Necessary Functions


emo = ['anger','fear' ,'joy' ,'sadness']

def pred_emotion(string, ret=None):
  '''
  If you give "ret" as either - model_output, emotion or dict, it'll retun the same (only that).
  But if you don't give it anything, it'll print all the values
  '''
  probs=list(tr_model.predict_proba([string])[0])

  if ret==None:
    print('Model output: ',tr_model.predict_proba([string])[0],'\n\n')
  elif ret=='model_output':
    return tr_model.predict_proba([string])[0]
  
  if ret==None:
    print('The Sentence is mostly {}'.format(emo[np.argmax(probs)]),'\n\n')
  elif ret=='emotion':
    return emo[np.argmax(probs)]

  emodict={k:'{:3f}%'.format(v*100) for (k,v) in zip(emo,probs)}
  if ret==None:
    print(emodict,'\n')
  elif ret=='dict':
    return emodict

'''
stri="I'll kill him now if I see his face!!"

pred_emotion(stri)

stri="Corona is dreadful"

pred_emotion(stri)#,'emotion')

stri="He's not your true friend"

pred_emotion(stri,'dict')

"""#**Taking Twitter Data** 
By scraping from tweepy through a search keyword
"""
'''


