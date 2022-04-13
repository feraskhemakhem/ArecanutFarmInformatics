# import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for
import rds_db as db

from datetime import datetime
from datetime import timedelta
#import email
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # if we get a form request to log in
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['password']
        try:
            user_id = db.get_user(username, password)
            return render_template('Landing.html')
        except Exception as e:
            return render_template('login.html', var=e)
        # if valid user_id, reroute to landing page of user
        return render_template('Landing.html')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    # if we get a form request to sign up
    if request.method == 'POST':
        username = request.form['Username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['password2']
        # call db function
        try:
            user_id = db.insert_new_user(username, email, password, confirm_password)
        except Exception as e:
            return render_template('signup.html', var=e)
        return render_template('home_page.html')
    return render_template('signup.html')

@app.route('/tankinput', methods=['GET', 'POST'])
def tank_input():
    # if we get a form request to add tank details

    return render_template('tankinput.html')

@app.route('/plotinput', methods=['GET','POST'])
def plot_input():
    if request.method == 'POST':
        plot_names = request.form.getlist('plot_name')
        if plot_names == []:
            return render_template('Landing.html')# return landing page
        plot_size = request.form.getlist('plot_size')
        #store these in db
        return render_template("irrigation_input.html", plot_names=plot_names)
    return render_template('plot_input.html')

@app.route('/irrigationschedule', methods=['GET','POST'])
def irrigation_schedule_input():
    if request.method == "POST":
        start_date = request.form.getlist('start_date')
        start_time = request.form.getlist('start_time')
        end_time = request.form.getlist('end_time')
        frequency = request.form.getlist('frequency')
        #save these in db
        return render_template('Landing.html')#landing page
    return render_template('irrigation_input.html')

@app.route('/rainfallinput', methods=['GET','POST'])
def rainfall_input():
    if request.method == "POST":
        _date = request.form.getlist('date')[0]
        _measurement = request.form.getlist('rainfall')[0]
        if not str(_date)<= str(datetime.today().date()):
            raise Exception('wrong date')
        try:
            _measurement = float(_measurement)
        except:
            raise Exception('wrong data type - rainfall input')

        
        #save these in db
        return render_template('Landing.html')#landing page


    return render_template('rainfall_input.html')



if '__main__' == __name__:
    app.run()
