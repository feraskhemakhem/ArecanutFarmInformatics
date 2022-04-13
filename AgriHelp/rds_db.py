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

# create table if not already existing (no encryption)
# cursor = conn.cursor()
# create_table = """
# CREATE TABLE IF NOT EXIST Users (user_id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, username VARCHAR(31) DEFUALT NULL, email VARCHAR(255) DEFAULT NULL, pswd VARCHAR(255) DEFAULT NULL)
# """
# cursor.execute(create_table)

"""
Iteration 1: User account functions
"""

# insert new user (no ecryption)
# exceptions: passwords do not match, username already exists
# return: user id if successful
def insert_new_user(username, email, password, password_verify):
    # if passwords do not match, return false
    if password != password_verify:
        raise Exception('Passwords do not match')
    # check if username already exists or insert new user account
    with conn.cursor() as curr:
        # check if username already exists
        curr.execute("SELECT * FROM Users WHERE username = %s", (username))
        user_details = curr.fetchone()
        if user_details: # if username already in use, return -2
            raise Exception('Username already in use')
        # otherwise, add new user
        curr.execute("INSERT INTO Users (username, email, pswd) VALUES (%s, %s, %s)",  (username, email, password))
        conn.commit()
        # now get user ID to return
        curr.execute("SELECT user_id FROM Users WHERE username = %s", (username))
        new_user = curr.fetchone()
        return int(new_user[0])
    # if connection failed return false
    # return False

# verify login info given username/password
# exceptions: user does not exist, password incorrect
# return: user id if valid
def get_user(username, password):
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
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM Users")
        user_list = curr.fetchall()

        return user_list



"""
Iteration 2: Rainfall, and Plot Inputs (Including Irrigation Schedule)
"""

# add new rainfall day
# parameters are string, list, list
def add_rainfall_day(username, _date, _rainfall_quant):
    date = _date[0]
    print(date)
    rainfall_quant = _rainfall_quant[0]
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

# add new plot input
# parameters are string, list, list
def add_plot(username, _plot_name, _plot_size):
    with conn.cursor() as curr:
        # if already exists and not the same val, replace it
        # if not in the table, add new entry
        for i in range(len(_plot_name)):
            plot_name = _plot_name[i]
            plot_size = _plot_size[i]
            curr.execute("SELECT plot_size FROM Plots WHERE username = %s AND plot_name = %s", (username, plot_name))
            plot_details = curr.fetchone()
            if plot_details and plot_details[0] != plot_size: # if already exists and not the same value
                print(plot_details)
                print(type(plot_details))
                curr.execute("UPDATE Plots SET plot_size = %s WHERE username = %s AND plot_name = %s", (plot_size, username, plot_name))
            elif not plot_details: # if does not exist, add new
                print("elif here")
                curr.execute("INSERT INTO Plots (username, plot_name, plot_size) VALUES (%s, %s, %s)", (username, plot_name, plot_size))
            # else, correct value already stored and do nothing!
            else:
                return
            # commit changes if not doing nothing
            conn.commit()

# add new plot input
# parameters are string, list, list
def add_irrigation_schedule(username, _plot_name, _start_date, _start_time, _end_time, _freq):
    print(_plot_name)
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

# get plot details
def get_plot(username):
    with conn.cursor() as curr:
        curr.execute("SELECT plot_name, plot_size FROM Plots WHERE username = %s", (username))
        plot_details = curr.fetchall()
        return plot_details

# get irrigation schedule details
def get_irrigation_schedule(username):
    with conn.cursor() as curr:
        curr.execute("SELECT start_date, start_time, end_time, frequency FROM Plots WHERE username = %s", (username))
        irrigation_details = curr.fetchall()
        return irrigation_details


"""
Iteration 3: Tank Input
"""

# add new tank to database
# all inputs are strings except dimensions, which is an array of strings
def add_tank_input(username, tank_name, tank_shape, dimensions):
    with conn.cursor() as curr:
        # the shape will determine the number of dimensions to populate
        # automatically populate the keyword string based on shape
        if (tank_shape == 'Rectangle'):
            curr.execute("INSERT INTO Tanks (username, tank_name, tank_shape, dimension_1, dimension_2, dimension_3) VALUES %s, %s, %s, %s, %s, %s", (username, tank_name, tank_shape, dimensions[0], dimensions[1], dimensions[2]))
        elif (tank_shape == 'Trapezoid'):
            curr.execute("INSERT INTO Tanks (username, tank_name, tank_shape, dimension_1, dimension_2, dimension_3, dimension_4, dimension_5) VALUES %s, %s, %s, %s, %s, %s, %s, %s", (username, tank_name, tank_shape, dimensions[0], dimensions[1], dimensions[2], dimensions[3], dimensions[4]))
        elif (tank_shape == 'Circle'):
            curr.execute("INSERT INTO Tanks (username, tank_name, tank_shape, dimension_1, dimension_2) VALUES %s, %s, %s, %s, %s", (username, tank_name, tank_shape, dimensions[0], dimensions[1]))
        curr.commit()


"""
Helper Functions
"""

# get DB
def get_db(table_name):
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM %s", (table_name))
        table_contents = curr.fetchall()
        print(table_contents)
