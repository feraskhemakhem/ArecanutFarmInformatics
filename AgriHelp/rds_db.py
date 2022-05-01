"""
Using pymysql to access the db on AWS RDS
"""

import pymysql
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

# connect to aws
conn = pymysql.connect(
        host = os.environ['HOST_NAME'],
        port = int(os.environ['PORT_NO']),
        user = os.environ['USER_NAME'],    
        password = os.environ['PASSWORD'],
        db = os.environ['DB'],
        )



def insert_new_user(username, email, password, password_verify):
    """
    Inserts new user into the database according to the above credentials. 
    Throws an error incase the user already exists.
    Throws an error if password or password2 dont match
    # Inputs
    username : username of the user
    email: email of the user
    password : password given by the new user
    password2: password given in the confirm password area by the new user 
    # Output
    user id or index of the user we assign internally in our db
    """

    # if passwords do not match throw exception.
    if password != password_verify:
        raise Exception('Passwords do not match')
    
    with conn.cursor() as curr:
    
        curr.execute("SELECT * FROM Users WHERE username = %s", (username))
        user_details = curr.fetchone()
        if user_details: 
            raise Exception('Username already in use')
        # otherwise, add new user
        curr.execute("INSERT INTO Users (username, email, pswd) VALUES (%s, %s, %s)",  (username, email, password))
        conn.commit()
        # now get user ID to return
        curr.execute("SELECT user_id FROM Users WHERE username = %s", (username))
        new_user = curr.fetchone()
        return int(new_user[0])
    



def get_user(username, password):
    """
    get the user id for a given user name and password details
    """
    with conn.cursor() as curr:
        # run query and get results
        curr.execute("SELECT user_id, pswd FROM Users WHERE username = %s", (username))
        user_details = curr.fetchone()
        # details is now a map of schema names to values
        # check if row exists or password doesn't match what's in mySQL
        if not user_details:
            raise Exception('Username does not exist')
        elif user_details[1] != password:
            raise Exception('Incorrect password')
        else:
            return user_details[0]

def get_user_list():
    """
    gives the list of all users present in our database
    """
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM Users")
        user_list = curr.fetchall()

        return user_list



def add_rainfall_day(username, _date, _rainfall_quant):
    """
    Adds the rainfall details for a given date to specified user
    """
    date = _date
    print(date)
    rainfall_quant = _rainfall_quant
    print(rainfall_quant)
    with conn.cursor() as curr:
        # if already exists and not the same val, replace it
        # if not in the table, add new entry
        curr.execute("SELECT rain_quant FROM Rainfall WHERE username = %s AND rain_date = %s", (username, date))
        rain_details = curr.fetchone()
        if rain_details and rain_details[0] != rainfall_quant: # if already exists and not the same value
            print(rain_details)
            print(type(rain_details))
            curr.execute("UPDATE Rainfall SET rain_quant = %s WHERE username = %s AND rain_date = %s", (rainfall_quant, username, date))
        elif not rain_details: # if does not exist, add new
            curr.execute("INSERT INTO Rainfall (username, rain_date, rain_quant) VALUES (%s, %s, %s)", (username, date, rainfall_quant))
        # else, correct value already stored and do nothing!
        else:
            return
        # commit changes if not doing nothing
        conn.commit()

def add_plot(username, _plot_name, _plot_size):
    """
    Adds a new plot and its details in the Plots table for a user
    """
    with conn.cursor() as curr:
        # if already exists and not the same val, replace it
        # if not in the table, add new entry

        curr.execute("DELETE FROM Plots WHERE username = %s;", (username))
        for each_plot_name,each_plot_size in zip(_plot_name,_plot_size):
            curr.execute("INSERT INTO Plots (username, plot_name, plot_size) VALUES (%s, %s, %s)", (username, each_plot_name, each_plot_size))
        conn.commit()



def add_irrigation_schedule(username, _plot_name, _start_date, _start_time, _end_time, _freq):
    """
    Adds irrigation schedule for a corresponding user and plot. 
    Takes in the start date, start time , end time,frequency and adds it to the database 
    which are further used to calculate irrigation schedule
    """
    
    with conn.cursor() as curr:
        # if already exists and not the same val, replace it
        # if not in the table, add new entry
        for i in range(len(_plot_name)):
            start_date = _start_date[i]
            plot_name = _plot_name[i]
            start_time = _start_time[i]
            end_time = _end_time[i]
            freq = _freq[i]
            # update db
            curr.execute("UPDATE Plots SET start_date = %s, start_time = %s, end_time = %s, frequency = %s WHERE username = %s AND plot_name = %s", (start_date, start_time, end_time, freq, username, plot_name))
        conn.commit()


def get_plot(username):
    """
    gives all plot details corresponding to a user
    """
    with conn.cursor() as curr:
        curr.execute("SELECT plot_name, plot_size FROM Plots WHERE username = %s", (username))
        plot_details = curr.fetchall()
        return plot_details

def get_irrigation_schedule(username):
    """
    returns the irrigation schedules of all plots corresponding to a user name
    """
    with conn.cursor() as curr:
        curr.execute("SELECT start_date, start_time, end_time, frequency FROM Plots WHERE username = %s", (username))
        irrigation_details = curr.fetchall()
        return irrigation_details



def add_tank_input(username, tank_name, tank_shape, dimensions):
    """
    adds new tank details corresponding to a username
    """
    with conn.cursor() as curr:
        # the shape will determine the number of dimensions to populate
        # automatically populate the keyword string based on shape
        if (tank_shape == 'rectangle'):
            curr.execute("INSERT INTO Tanks (username, tank_name, tank_shape, dimension_1, dimension_2, dimension_3) VALUES (%s, %s, %s, %s, %s, %s)", (username, tank_name, tank_shape, dimensions[0], dimensions[1], dimensions[2]))
        elif (tank_shape == 'trapezoid'):
            curr.execute("INSERT INTO Tanks (username, tank_name, tank_shape, dimension_1, dimension_2, dimension_3, dimension_4, dimension_5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (username, tank_name, tank_shape, dimensions[0], dimensions[1], dimensions[2], dimensions[3], dimensions[4]))
        elif (tank_shape == 'circle'):
            curr.execute("INSERT INTO Tanks (username, tank_name, tank_shape, dimension_1, dimension_2) VALUES (%s, %s, %s, %s, %s)", (username, tank_name, tank_shape, dimensions[0], dimensions[1]))
        conn.commit()



def get_db(table_name):
    """
    get details corresponding to db
    """
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM %s", (table_name))
        table_contents = curr.fetchall()
        print(table_contents)
