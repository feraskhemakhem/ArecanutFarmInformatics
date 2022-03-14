"""
Using pymysql to access the db on AWS RDS
"""

import pymysql
from dotenv import dotenv_values

# load env variables
config = dotenv_values('.env')

# connect to aws
conn = pymysql.connect(
        host = config['HOST'],
        port = int(config['PORT']),
        user = config['USER'],    
        password = config['PASSWORD'],
        db = config['DB'],
        )

# create table if not already existing (no encryption)
# cursor = conn.cursor()
# create_table = """
# CREATE TABLE IF NOT EXIST Users (user_id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, username VARCHAR(31) DEFUALT NULL, email VARCHAR(255) DEFAULT NULL, pswd VARCHAR(255) DEFAULT NULL)
# """
# cursor.execute(create_table)

# insert new user (no ecryption)
# -1: passwords do not match
# -2: username already exists
#  0: works
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
def get_user(username, password):
    with conn.cursor() as curr:
        # run query and get results
        curr.execute("SELECT user_id, pswd FROM Users WHERE username = %s", (username))
        user_details = curr.fetchone()
        # details is now a map of schema names to values
        # check if row exists or password doesn't match what's in mySQL
        print(user_details)
        if not user_details:
            raise Exception('Username does not exist')
        elif user_details[1] != password:
            raise Exception('Incorrect password')
        else:
            return user_details[0]
