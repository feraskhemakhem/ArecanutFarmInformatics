from unicodedata import name
import pymysql
import datetime 
import smtplib
from dotenv import load_dotenv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import collections
import os


# connect to aws
load_dotenv()
conn = pymysql.connect(
        host = os.environ['HOST_NAME'],
        port = int(os.environ['PORT_NO']),
        user = os.environ['USER_NAME'],    
        password = os.environ['PASSWORD'],
        db = os.environ['DB'],
        )

def get_data_for_scheduling():
    """
    Gets all the details of the user and corresponding plot details present in db
    """
    query = "select username,email,plot_name,start_date,start_time,frequency from Plots inner join (select username as u , email from Users) as a where a.u=username"
    output = []
    with conn.cursor() as curr:
        curr.execute(query )
        plot_details = list(curr.fetchall())
        description  = [k[0] for k in curr.description]
        
        for each in plot_details:
            output.append({des:det for (det,des) in zip(each,description)})
        
    return output


def give_emailing_rows(data):
    """
    gives the rows in data for which we have to send emails today.
    """
    current_date = datetime.datetime.today().date()
    output = []
    for each_row in data:
        if each_row['start_date'] is not None:
            diff = (current_date-each_row['start_date']).days
            if diff%each_row['frequency']==0:
                output.append(each_row)
    return output

def email(data):
    """
    send emails to all rows present in the data
    """

    names = getCol(data,'username') #name array
    emails = getCol(data,'email') #email array
    plot_names = getCol(data,'plot_name') #plot names array
    start_times = getCol(data,'start_time') # start time array


    
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(os.environ['EMAIL'],os.environ['SENDER_PASS'])
    
    for name,email,plot,start_time in zip(names,emails,plot_names,start_times):
        msg = MIMEMultipart()
        html = """\
            <html>
                <body style="background-color:#D4D6CF;">
                    <span style="opacity: 0"> {{ randomness }} </span>
                    <h1 style="color:#DBA40E;">Irrigation Reminder</h1>
                   <h2 style="color:#013A20;">Hello """+str(name)+""" User</h2>
                    <p><h3 style="color:#3F4122;">This is a friendly reminder that your irrigation is scheduled at <br>
                     """ +str(start_time)+ """ in plot """ +str(plot)+ """
                    </h3></p>
                    <span style="opacity: 0"> {{ randomness }} </span>
                 </body>
            </html>
            """
        temp = MIMEText(html, 'html')
        msg['From']='Agrihelp Team'
        msg['To']= email
        msg['Subject'] ="Upcoming Irrigation Reminder"
        msg.attach(temp)
        s.send_message(msg)

        
    # Terminate the SMTP session and close the connection
    s.quit()

def flatten(x):
    """flattens the dictionary"""
    try:
        collectionsAbc = collections.abc
    except AttributeError:
        collectionsAbc = collections

    if isinstance(x, dict) :
        return [x]
    elif isinstance(x, collectionsAbc.Iterable) :
        return [a for i in x for a in flatten(i)]
    else:
        return [x]

def getCol(data,col):
    """
    takes in the data , and the col name , and converts values
    corresponding to the col name into a list and returns it
    """
    data = flatten(data)
    ans = []
    for curr in data:
        ans.append(curr[col])
    return ans

def execute():
    """
    executes the scheduling email function
    """
    #get data from database
    ans = get_data_for_scheduling()
    
    #checks which emails to send today by comparing date and frequency
    temp = give_emailing_rows(ans)
    
    email(temp)

if __name__ == '__main__':
    execute()


  
