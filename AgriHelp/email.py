from datetime import date
#from dateutil.relativedelta import relativedelta
import rds_db as db
# from flask import Flask, render_template, request, redirect, url_for

# starts_at = date(2010, 1, 1)
# today = date(2010, 2, 1)  # as an example
# diff = relativedelta(today, starts_at)
#
# if diff.days == 0:  # there must be no days difference between two dates
#     if diff.months % 12 == 0:  # this is a year interval
#         do_something('annual')
#     elif diff.months % 6 == 0:  # this is a six month interval
#         do_something('bi_annual')
#     elif diff.months % 3 == 0:  # this is a three month interval
#         do_something('quarter')
#     else:  # this is a month interval
#         do_something('month')
def email():
    #_username, _email, _pswd = get_user_list()
    user_list = db.get_user_list()
    for user in user_list:
        _userid, _username, _email, _pswd = user
        print(user)


#return next available date
# def desired_date(_):
#     start_date, start_time,end_time,frequency =
#         _plot_names, _plot_sizes = get_plot_info(username)
#         n = range(1, len(_plot_names)+1)
#         _start_date, _start_time, _end_time, _frequency = get_irrigation_info(username)
if __name__ == '__main__':
    email()
