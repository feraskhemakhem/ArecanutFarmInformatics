# import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for
import rds_db as db

from datetime import datetime
from datetime import timedelta
import email
app = Flask(__name__)
global username

def get_irrigation_info(username):
    """
    gives the list of start dates , start times, endtimes,frequency 
    of plots corresponding to the given user
    """
    _irrigation_info = db.get_irrigation_schedule(username)
    _start_date = [i[0] for i in _irrigation_info]
    _start_time = [i[1] for i in _irrigation_info]
    _end_time = [i[2] for i in _irrigation_info]
    _frequency = [i[3] for i in _irrigation_info]
    return _start_date, _start_time, _end_time, _frequency

def get_plot_info(username):
    """
    gives list of plotnames, plot sizes of plots corresponding to a given user
    """
    _plot_info = db.get_plot(username)
    _plot_names = [i[0] for i in _plot_info]
    _plot_sizes = [i[1] for i in _plot_info]
    return _plot_names, _plot_sizes



@app.route('/')
def home_page():
    """renders home page"""
    return render_template('home_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    this function takes in the user credentails(for logging in), checks them that
    it is a valid user and renders the landing page on submission.
    """
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
    """
    This page takes in the signup credentials of the new user, inserts them to the db,
    renders the landing page on submission
    """
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
    """
    This function takes in the tank details , saves them to the db 
    and renders landing page on submission
    """
    # if we get a form request to add tank details
    global username
    if request.method == 'POST':
        _tank_name = request.form.get('tank_name')
        _tank_shape = request.form.get('TANK')
        _tank_dimensions = []
        print(_tank_name, _tank_shape)
        if _tank_shape == 'circle':
            circ_dia = request.form.get('diameter')
            circ_ht = request.form.get('cheight')
            _tank_dimensions.extend([circ_dia, circ_ht])
        elif _tank_shape == 'rectangle':
            rect_l = request.form.get('length')
            rect_d = request.form.get('depth')
            rect_w = request.form.get('width')
            _tank_dimensions.extend([rect_l, rect_d, rect_w])
        else:
            trap_t1 = request.form.get('top1')
            trap_t2 = request.form.get('top2')
            trap_b1 = request.form.get('base1')
            trap_b2 = request.form.get('base2')
            trap_ht = request.form.get('height')
            _tank_dimensions.extend([trap_t1, trap_t2, trap_b1,trap_b2, trap_ht])
        try:
            db.add_tank_input(username, _tank_name, _tank_shape, _tank_dimensions)
            #print("Tank input added successfully")
        except Exception as e:
            #print(e)
            return render_template('tank_input.html', var=e)
        return render_template('landing.html', variable=username)

    return render_template('tank_input.html', variable=username)

@app.route('/plotinput', methods=['GET','POST'])
def plot_input():
    """
    This function takes in the new plot details , adds them to the database
    and renders the irrigation input page on submission.
    """
    global username
    _plot_names, _plot_sizes = get_plot_info(username)
    n = range(1, len(_plot_names)+1)
    _start_date, _start_time, _end_time, _frequency = get_irrigation_info(username)

    if request.method == 'POST':
        _plot_names = request.form.getlist('plot_name')
        if _plot_names == []:
            return render_template('landing.html', variable=username)# return landing page

        if len(_plot_names)!=len(set(_plot_names)):
            return render_template('plot_input.html', rownum=len(_plot_names),
                           plot_info=zip(n, _plot_names,_plot_sizes), variable=username,
                           message='Conflicting plot names', condition=True)

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
                           plot_info=zip(n, _plot_names,_plot_sizes), variable=username, condition=False)

@app.route('/irrigationschedule', methods=['GET','POST'])
def irrigation_schedule_input():
    """
    This function fetches the irrigation schedule data, corresponding to the plots
    of a user, saves it to the database , and renders the landing page. This whole
    process is done on submission
    """
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
    """
    This function, fetches the rainfall data , date data from the form 
    and saves it to the database. It also renders landing page template
    on submission
    """
    global username
    if request.method == "POST":
        _date = request.form.getlist('date')[0]
        _measurement = request.form.getlist('rainfall')[0]
        if not str(_date)<= str(datetime.today().date()):
            raise Exception('wrong date')
        try:
            _measurement = float(_measurement)
        except:
            raise Exception('wrong data type - rainfall input')

        db.add_rainfall_day(username, _date, _measurement)
        #save these in db
        return render_template('landing.html', variable=username)#landing page


    return render_template('rainfall_input.html', varaible=username)

if '__main__' == __name__:
    app.run()
