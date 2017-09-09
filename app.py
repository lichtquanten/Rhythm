from flask import Flask, render_template, url_for, current_app, request
import os
import nlp

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def postData():
    text = request.form['text']
    nlp.splitString(text)
    return render_template('index.html', algorithm=text, action=nlp.ac.toString(), condition=nlp.con.toString())

if __name__ == '__main__':
    app.run()