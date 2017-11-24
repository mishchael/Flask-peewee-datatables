#!/usr/bin/env python3
# -*- coding:utf-8 -*-
U"""
main flask app
"""

from flask import Flask
from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension
from src.api import api


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'example'
toolbar = DebugToolbarExtension(app)

app.register_blueprint(api, url_prefix="/api")


@app.route("/")
def index():
    return render_template("test.html")


if __name__ == '__main__':
    app.run(threaded=True)
