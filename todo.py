# -*- coding: utf-8 -*-

import os, sys, json
from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_object(__name__)

def read_file(source_file):
    """open file for get list of TODO in dictionary
    Arguments:
    - `source_file`: source file
    """
    try:
        return json.load(open(source_file, 'r'))
    except:
        return False

app = Flask(__name__)
app.config.from_object(__name__)
        
@app.route('/')
def index():
    """view for user"""
    return render_template('index.html')   

if __name__ == "__main__":
    app.run(debug=True)
