#!/usr/bin/python2.7

############################
#  TO DO
############################
# - read from org-mode file / txt file
# - shutdown the program 
import smtplib
import getpass
import os
import re
import time #this will be deleted

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime 
from pytz import timezone

def request_id():
    mail = raw_input('gmail user >> ')
    password = getpass.getpass('password >> ')

    return mail + '@gmail.com', password

def request_list():
    print 'Add items to your list:'
    print "write 'done' when you list is complete:"
    item = raw_input('>> ')
    my_list = ''
    while (item != 'done'):
        my_list += (' - ' + item + '\n')
        item = raw_input('>> ')

    return my_list

class Gmail_api(object):
    def __init__(self):
        self.email, self.password = request_id()
        self.server = 'smtp.gmail.com'
        self.port = 587
        
        session = smtplib.SMTP(self.server, self.port)
        session.ehlo() #Identify yourself to the server. 
        session.starttls() # Transport layer security
        try: 
            session.login(self.email, self.password)
        except smtplib.SMTPAuthenticationError:
            print 'Invalid user/password ... try again'
            self.email, self.password = request_id()

        self.session = session

    def send_message(self):
        headers = [
                "From: " + self.email,
                "Subject: Shopping List" ,
                "To: " + self.receiver,
                "Content-Type: text/plain"
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
        #self.body = raw_input('Food List >> ')
        self.body = request_list()

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
