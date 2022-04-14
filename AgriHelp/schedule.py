import pymysql
import datetime 
import smtplib

from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# load env variables
config = dict(
    HOST_NAME="arecanutfarminformatics.ceyu5qc2r3bs.us-east-1.rds.amazonaws.com",
PORT_NO="3306",
USER_NAME="admin",
PASSWORD="0HfVq0WFEX0zrKBDK5hz",
DB="Farm_Informatics"

)
# connect to aws
conn = pymysql.connect(
        host = config['HOST_NAME'],
        port = int(config['PORT_NO']),
        user = config['USER_NAME'],
        password = config['PASSWORD'],
        db = config['DB'],
        )


def get_data_for_scheduling():
    query = "select username,plot_name,start_date,start_time,frequency,email from Plots inner join (select username as u , email from Users) as a where a.u=username"
    output = []
    with conn.cursor() as curr:
        curr.execute(query )
        plot_details = list(curr.fetchall())
        description  = [k[0] for k in curr.description]
        
        for each in plot_details:
            output.append({des:det for (det,des) in zip(each,description)})
        
    return output

def give_emailing_rows(data):
    current_date = datetime.datetime.today().date()
    output = []
    for each_row in data:
        diff = (current_date-each_row['start_date']).days
        if diff%each_row['frequency']==0:
            output.append(each_row)
    return output




def sending_emails(data):
    # set up the SMTP server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login('rimsha.maredia98@gmail.com', 'Rimsha123')

    
    names = ['siri']
    emails  = ['siri.pranitha1012@gmail.com']
    
    
    # For each contact, send the email:
    for each_row in data:
        msg = MIMEMultipart()      
        message = f"This is friendly reminder to water the irrigation plot {each_row['plot_name']} at time {str(each_row['start_time'])} today\n\nRegards,\nArecanut Farm Informatics"
        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']= 'Arecanut Farm Informatics'
        msg['To']= each_row['email']
        msg['Subject']=f"Irrigation reminder for {each_row['plot_name']} "
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        server.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    server.quit()
    
def send_email():
    email_user = 'rimsha.maredia@gmail.com'
    server = smtplib.SMTP ('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, 'email pass')

    #EMAIL
    message = 'sending this from python!'
    server.sendmail(email_user, email_user, message)
    server.quit()

def email():
    names = ['siri']
    emails  = ['siri@tamu.edu']
    #message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login('Agrihelp2022@gmail.com', 'mission2022@')

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()      
        message = 'This is a friendly reminder that your irrigation is scheduled from 9:00am to 12:00pm'
        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=name
        msg['To']=email
        msg['Subject']="Upcoming Irrigation Reminder"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()




if __name__ == '__main__':
    email()
