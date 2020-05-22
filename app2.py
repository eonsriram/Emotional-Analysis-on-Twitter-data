
#Flask APP

from flask import Flask, render_template, url_for, redirect, request, flash
import requests
from emotionalanalysis import pred_emotion

app = Flask(__name__)

app.config['SECRET_KEY']="alohomora"

#Routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/EmotionalAnalysis')
def eahome():
    return render_template('EAhome.html')

@app.route('/Real-Time-Analysis')
def realtime():
    return render_template('realtime.html')

@app.route('/Text-Analysis')
def text():
    return render_template('text.html')


@app.route('/protext', methods=['POST'])
def protext():
    
    sentence= request.form['senttext']

    emotions=pred_emotion(sentence,ret="dict")

    out0="The emotions are :"
    out1="Anger : "+ str(list(emotions.values())[0])
    out2="Fear : "+ str(list(emotions.values())[1])
    out3="Joy : "+ str(list(emotions.values())[2])
    out4="Sadness : "+ str(list(emotions.values())[3])

    flash(out0)
    flash(out1)
    flash(out2)
    flash(out3)
    flash(out4)
    
    return render_template('text.html')


if __name__ == "__main__":
    app.run(debug = True)