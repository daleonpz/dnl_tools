#!/usr/bin/python2.7

############################
#  TO DO
############################
# - add food list
# - read from org-mode file / txt file
# - create a method for get the data ( receiver, food and time)
import smtplib
import getpass
import os
import re
import time #this will be deleted

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime 
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

    def send_message(self):
        headers = [
                "From: " + self.email,
                "Subject: Shopping List" ,
                "To: " + self.receiver,
                "Content-Type: text/html"
                ]
        headers = "\r\n".join(headers)

        # sendmail( sender, receiver, message)
        self.session.sendmail(
                self.email,
                self.receiver,
                headers + "\r\n\r\n" + self.body
                )

    def get_data(self):
        self.receiver = raw_input('To >> ')
        self.body = raw_input('Food List >> ')

        # The input should be something like this 18:45
        timer = raw_input('Set alarm, 24Hrs format >> ')
        timer = map(int,re.split(":",timer))
        now = datetime.now()
        self.alarm = now.replace(hour=timer[0], minute=timer[1])
        print self.alarm

    def run_scheduler(self):
        scheduler = BackgroundScheduler()

        scheduler.add_job( 
                self.send_message,
                'date',
                run_date = self.alarm )
        
        scheduler.start()

        try:
        # This is here to simulate application activity (which keeps the main thread alive).
        # need to finish the thread after accomplish the job
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
                scheduler.shutdown()
#        


######################################
#      M A I N
######################################

gm = Gmail_api()
gm.get_data()
gm.run_scheduler()

