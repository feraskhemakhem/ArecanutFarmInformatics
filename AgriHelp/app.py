# import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for
import rds_db as db

app = Flask(__name__)
global username

def get_irrigation_info(username):
    _irrigation_info = db.get_irrigation_schedule(username)
    _start_date = [i[0] for i in _irrigation_info]
    _start_time = [i[1] for i in _irrigation_info]
    _end_time = [i[2] for i in _irrigation_info]
    _frequency = [i[3] for i in _irrigation_info]
    return _start_date, _start_time, _end_time, _frequency

def get_plot_info(username):
    _plot_info = db.get_plot(username)
    _plot_names = [i[0] for i in _plot_info]
    _plot_sizes = [i[1] for i in _plot_info]
    return _plot_names, _plot_sizes
    
    

@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    global username
    # if we get a form request to log in
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['password']
        try:
            user_id = db.get_user(username, password)
            print("user logged in succesesfully")
            # if valid user_id, reroute to landing page of user
            # return render_template('landing.html',variable=username)
            return render_template('landing.html',variable=username)
        except Exception as e:
            return render_template('login.html', var=e)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    # if we get a form request to sign up
    global username
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
        return render_template('landing.html', variable=username)
    return render_template('signup.html')

@app.route('/tankinput', methods=['GET', 'POST'])
def tank_input():
    # if we get a form request to add tank details
    if request.method == 'POST':
        _tank_name = request.form.get('tank_name')
        #need to see how to pick and send values to get stored (based on table struct)
        #_measurement = request.form.getlist('')
        
    return render_template('tankinput.html')

@app.route('/plotinput', methods=['GET','POST'])
def plot_input():
    global username
    _plot_names, _plot_sizes = get_plot_info(username)
    n = range(1, len(_plot_names)+1)
    _start_date, _start_time, _end_time, _frequency = get_irrigation_info(username)

    if request.method == 'POST':
        _plot_names = request.form.getlist('plot_name')
        if _plot_names == []:
            return render_template('landing.html', variable=username)# return landing page
        _plot_sizes = request.form.getlist('plot_size')
        #store these in db
        db.add_plot(username, _plot_names, _plot_sizes)
        
        _start_date = _start_date + ['' for i in _plot_names]
        _start_time = _start_time + ['' for i in _plot_names]
        _end_time = _end_time + ['' for i in _plot_names]
        _frequency = _frequency + ['' for i in _plot_names]
        
        return render_template("irrigation_input.html", 
                               info=zip(_plot_names,_start_date,_start_time, _end_time, _frequency), 
                               variable=username)
    
    return render_template('plot_input.html', rownum=len(_plot_names),
                           plot_info=zip(n, _plot_names,_plot_sizes), variable=username)

@app.route('/irrigationschedule', methods=['GET','POST'])
def irrigation_schedule_input():
    global username
    _plot_names, _plot_sizes = get_plot_info(username)
    _start_date, _start_time, _end_time, _frequency = get_irrigation_info(username)
    if request.method == "POST":
        start_date = request.form.getlist('start_date')
        start_time = request.form.getlist('start_time')
        end_time = request.form.getlist('end_time')
        frequency = request.form.getlist('frequency')
        #save these in db
        db.add_irrigation_schedule(username, _plot_names, start_date, start_time, end_time, frequency)
        return render_template('landing.html', variable=username)#landing page
    return render_template("irrigation_input.html", 
                               info=zip(_plot_names,_start_date,_start_time, _end_time, _frequency), 
                               variable=username)

@app.route('/rainfallinput', methods=['GET','POST'])
def rainfall_input():
    global username
    if request.method == "POST":
        _date = request.form.getlist('date')
        _measurement = request.form.getlist('rainfall')
        #save these in db
        db.add_rainfall_day(username, _date, _measurement)
        return render_template('landing.html', variable=username)#landing page
    return render_template('rainfall_input.html', variable=username)

# @app.route('/LandingPage',method=["POST"])
# def LandingPage():
#     if request.method == "POST":
#         if request.form.get('Rainfall') == 'Rainfall_data':
#             return render_template('tankinput.html')
#         elif request.form.get('tankinput') == 'tankinput_data':
#             return render_template('tankinput.html')
#         else:
#             return render_template('home_page.html')


if '__main__' == __name__:
    app.run()
