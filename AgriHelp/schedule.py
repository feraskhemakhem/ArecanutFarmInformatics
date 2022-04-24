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
    query = "select username,email,plot_name,start_date,start_time,frequency from Plots inner join (select username as u , email from Users) as a where a.u=username"
    output = []
    with conn.cursor() as curr:
        curr.execute(query )
        plot_details = list(curr.fetchall())
        description  = [k[0] for k in curr.description]
        
        for each in plot_details:
            output.append({des:det for (det,des) in zip(each,description)})
        
    return output

#get rows from get_data_for_scheduling
def give_emailing_rows(data):
    current_date = datetime.datetime.today().date()
    output = []
    for each_row in data:
        diff = (current_date-each_row['start_date']).days
        if diff%each_row['frequency']==0:
            output.append(each_row)
    return output

def send_email():
    email_user = 'rimsha.maredia@gmail.com'
    server = smtplib.SMTP ('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, 'email pass')

    #EMAIL
    message = 'sending this from python!'
    server.sendmail(email_user, email_user, message)
    server.quit()

def email(data):

    names = getCol(data,'username')
    emails = getCol(data,'email')
    plot_names = getCol(data,'plot_name')
    start_times = getCol(data,'start_time')


    #message_template = read_template('message.txt')

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
                   <h2 style="color:#013A20;">Hello XYZ User</h2>
                    <p><h3 style="color:#3F4122;">This is a friendly reminder that your irrigation is scheduled at <br>
                     """ +str(start_time)+ """ in plot """ +str(plot)+ """
                    </h3></p>
                    <span style="opacity: 0"> {{ randomness }} </span>
                 </body>
            </html>
            """
        temp = MIMEText(html, 'html')
        message = 'Hello ' + name + ' This is a friendly reminder that your irrigation is scheduled at ' + str(start_time) + ' in plot ' + str(plot)
        print(message)
        message = str(message)
        msg['From']='Agrihelp Team'
        msg['To']= email
        msg['Subject'] ="Upcoming Irrigation Reminder"
        message = MIMEText(message)
        msg.attach(temp)
        s.send_message(msg)

        #del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

def flatten(x):
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
    data = flatten(data)
    ans = []
    for curr in data:
        ans.append(curr[col])
    return ans

if __name__ == '__main__':
    #email()
    #0 6 * * *" 
    ans = get_data_for_scheduling()
    temp = give_emailing_rows(ans)
    email(temp)


  