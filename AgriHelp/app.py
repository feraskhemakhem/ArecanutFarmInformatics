# import the Flask class from the flask module
from flask import Flask, render_template, request

import db

# create the application object
app = Flask(__name__)


# use decorators to link the function to a url
@app.route('/')
def home_page():
    return render_template('base.html')

@app.route('/login', methods=['post'])
def login_page():
    # if we get a form request to log in
    if request.method == 'POST':
        username = request.form('Username')
        password = request.form('password')
        # user_id is the ID corresponding to that user
        user_id = db.get_user(username, password)
        if user_id < 0: # if invalid user_id, let them know then do nothing
            print('Error: invalid authentication')
        else: # TODO: if valid user_id, reroute to landing page of user
            print(user_id)
    return render_template('login.html', var=user_id)

@app.route('/signup', methods=['post'])
def signup_page():
    # if we get a form request to sign up
    if request.method == 'POST':
        username = request.form('Username')
        email = request.form('email')
        password = request.form('password')
        confirm_password = request.form('password2')
        # call db function
        user_id = db.insert_new_user(username, email, password, confirm_password)
        if user_id == -1: # if passwords do not match
            print('Passwords do not match')
        elif user_id == -2: # username already in use
            print('Username already in use')
        else: # user added!
            print(user_id)
    return render_template('signup.html', var=user_id)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()
