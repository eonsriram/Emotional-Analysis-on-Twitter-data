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
    return render_template('EAHome.html')

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











@app.route('/inst')
def inst():
    return render_template('inst.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')    

@app.route('/q1')
@app.route('/OEYQ====')
def q1():
    return render_template('testq1.html')

@app.route('/q2')
@app.route('/OEZA====')
def q2():
    return render_template('testq2.html')

@app.route('/q3')
@app.route('/OEZQ====')
def q3():
    return render_template('testq3.html')

@app.route('/corr')
@app.route('/MNXXE4TFMN2A====')
def correct():
    return render_template('correct.html')

@app.route('/q4')
@app.route('/OE2A====')
def q4():
    return render_template('testq4-1.html')

@app.route('/treasurehuntv1.0')
def error1():
    return render_template('errorpage.html')

@app.route('/404')
def error2():
    return render_template('errorpageanswer.html')

@app.route('/q5')
@app.route('/OE2Q====')
def q5():
    return render_template('testq5.html')

@app.route('/q6')
@app.route('/OE2B====')
def q6():
    return render_template('testq6.html')

@app.route('/q7')
@app.route('/OE2X====')
def q7():
    return render_template('q7.html')

@app.route('/q8')
@app.route('/OE3X====')
def q8():
    return render_template('q8.html')

@app.route('/q9')
@app.route('/OE4G====')
def q9():
    return render_template('q9.html')

@app.route('/q10')
@app.route('/OE5C====')
def q10():
    return render_template('q10.html')

@app.route('/q11')
@app.route('/OE5E====')
def q11():
    return render_template('q11.html')

@app.route('/q12')
@app.route('/OE7X====')
def q12():
    return render_template('q12.html')

@app.route('/finish')
def finish():
    return render_template('finish.html')





#Process

@app.route('/pro1', methods=['POST'])
def pro1():
    if request.form['Answer'].lower()=="welcome":
        return redirect(url_for('q2'))
    else:
        flash("You are wrong!! Try again.")
    return redirect(url_for('q1'))
        #return redirect(url_for('wrong'))  

@app.route('/pro2', methods=['POST'])
def pro2():
    if request.form['Answer'].lower()=="98":
        return redirect(url_for('q3'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q2'))

@app.route('/pro3', methods=['POST'])
def pro3():
    if request.form['Answer'].lower()=="omega":
        return redirect(url_for('q4'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q3'))

@app.route('/pro4', methods=['POST'])
def pro4():
    if request.form['Answer'].lower()=="berlin":
        return redirect(url_for('q5'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q4'))

@app.route('/pro5', methods=['POST'])
def pro5():
    if request.form['Answer'].lower()=="you are an idiot":
        return redirect(url_for('q6'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q5'))

@app.route('/pro6', methods=['POST'])
def pro6():
    if request.form['Answer'].lower()=="not available":
        return redirect(url_for('q7'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q6'))
    
@app.route('/pro7', methods=['POST'])
def pro7():
    if request.form['Answer'].lower()=="enilsihtesrever":
        return redirect(url_for('q8'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q7'))

@app.route('/pro8', methods=['POST'])
def pro8():
    if request.form['Answer'].lower()=="coronavirus":
        return redirect(url_for('q9'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q8'))

@app.route('/pro9', methods=['POST'])
def pro9():
    if request.form['Answer'].lower()=="05214-8455-3" or request.form['Answer'].lower()=="0521484553" :
        return redirect(url_for('q10'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q9'))

@app.route('/pro10', methods=['POST'])
def pro10():
    if request.form['Answer'].lower()=="heart" :
        return redirect(url_for('q11'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q10'))

@app.route('/pro11', methods=['POST'])
def pro11():
    if request.form['Answer'].lower()=="200" :
        return redirect(url_for('q12'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q11'))

@app.route('/pro12', methods=['POST'])
def pro12():
    if request.form['Answer'].lower()=="groot" :
        return redirect(url_for('finish'))
    else:
        flash("Wrong...!! Try Again...!!")
    return redirect(url_for('q12'))



if __name__ == "__main__":
    app.run(debug = True)