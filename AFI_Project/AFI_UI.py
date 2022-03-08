# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a Python script file.
Author : Sindura Saraswathi
Date: 3/7/2022
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('base.html')


if '__main__' == __name__:
    app.run()