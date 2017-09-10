from flask import Flask, render_template, url_for, current_app, request
import os
import json
import nlp
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.static_folder = 'static'

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def postData():
    text = request.form['text']
    nlp.splitString(text)
    return render_template('index.html', algorithm=text, action=nlp.ac.toString(), condition=nlp.con.toString())

@app.route('/api', methods=['GET'])
def getNLP():
    message = request.args['text']
    print(message)
    return json.dumps(nlp.splitString(message)[0])

if __name__ == '__main__':
    app.run()