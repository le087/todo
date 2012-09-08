# -*- coding: utf-8 -*-

import os, json, uuid
from flask import Flask, request, render_template

# configuration
DATABASE = os.path.abspath('.') + '/data.json'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """view for user"""
    try:
        data = json.load(open(DATABASE, 'r'))
    except:
        data = {u"none":u"Добавьте больше записей"}
    if request.method == "POST":
        if request.form.has_key("add_note") and request.form["add_note"]:
            data[(str(uuid.uuid1()))[0:7]]=request.form["what_do"]
            json.dump(data, open(DATABASE, 'w')) 
            return render_template('index.html', list_todo=data)
        key = str(request.form.keys()[0])
        if data.has_key(key) and request.form[key]:
            del data[key]
            json.dump(data, open(DATABASE, 'w')) 
            return render_template('index.html', list_todo=data)
        else:
            return render_template('index.html', list_todo=data)
    else:
        return render_template('index.html', list_todo=data)

if __name__ == "__main__":
    app.run(debug=True)
