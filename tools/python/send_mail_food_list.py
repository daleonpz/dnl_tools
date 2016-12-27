#!/usr/bin/python2.7

############################
#  TO DO
############################
# - add food list
# - read from org-mode file / txt file
# - create a method for get the data ( receiver, food and time)
# - modify send message method
import smtplib
import getpass
import os

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from pytz import timezone

def ask_id():
    mail = raw_input('gmail user >> ')
    password = getpass.getpass('password >> ')

    return mail + '@gmail.com', password

class Gmail_api(object):
    def __init__(self):
        self.email, self.password = ask_id()
        self.server = 'smtp.gmail.com'
        self.port = 587
        
        session = smtplib.SMTP(self.server, self.port)
        session.ehlo() #Identify yourself to the server. 
        session.starttls() # Transport layer security
        try: 
            session.login(self.email, self.password)
        except smtplib.SMTPAuthenticationError:
            print 'Invalid user/password ... try again'
            self.email, self.password = ask_id()

        self.session = session

    def send_message(self, receiver, subject, body):
        headers = [
                "From: " + self.email,
                "Subject: " + subject,
                "To: " + receiver,
                "Content-Type: text/html"
                ]
        headers = "\r\n".join(headers)

        # sendmail( sender, receiver, message)
        self.session.sendmail(
                self.email,
                receiver,
                headers + "\r\n\r\n" + body
                )

gm = Gmail_api()
receiver = raw_input('To >> ')
scheduler = BackgroundScheduler()
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

scheduler.add_job( 
        gm.send_message,
        'date',
#        run_date='2016-12-25 21:08:05',
       # run_date = datetime.now().strftime(fmt),
        run_date = (datetime.now() + timedelta(minutes=0.5))) ,
        args=[receiver, 'To buy', 'Body'] )
scheduler.start()
#scheduler.remove('job')

import time
try:
    # This is here to simulate application activity (which keeps the main thread alive).
    # need to finish the thread after accomplish the job
    while True:
            time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
#os._exit(1)

#gm.send_message(receiver, 'To buy', 'This is the body')

