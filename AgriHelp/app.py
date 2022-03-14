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


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/login/', methods=["POST"])
def login_check():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pwd']
        return '<p>User logged in</p>'


@app.route('/signup')
def sign_up():
    return render_template('SignUp.html')

@app.route('/createaccount', methods=["POST"])
def create_account():
    if request.method == 'POST':
        username = request.form['Username']
        email = request.form['email']
        password = request.form['password']
        return '<p>User account created and logged in</p>'


if '__main__' == __name__:
    app.run()