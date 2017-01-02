#!/usr/bin/python2.7

############################
#  TO DO
############################
# - read from org-mode file / txt file
import smtplib
import getpass
import re
import time, sched

from datetime import timedelta, datetime

###################################
#   F u n c t i o n s
###################################
def request_id():
    mail = raw_input('gmail user >> ')
    password = getpass.getpass('password >> ')

    return mail + '@gmail.com', password

def request_list():
    print 'Add items to your list:'
    print "write 'done' when your list is complete:"
    item = raw_input('>> ')
    my_list = ''
    while (item != 'done'):
        my_list += (' - ' + item + '\n')
        item = raw_input('>> ')

    return my_list

def open_session(server, port):
        session = smtplib.SMTP(server, port)
        session.ehlo() #Identify yourself to the server. 
        session.starttls() # Transport layer security
        
        return session

##################################
#  C l a s s e s  D e f .
##################################

class Gmail_api(object):
    def __init__(self):
        self.email, self.password = request_id()
        self.server = 'smtp.gmail.com'
        self.port = 587
        
        session = open_session(self.server, self.port)

        try: 
            session.login(self.email, self.password)
        except smtplib.SMTPAuthenticationError:
            print 'Invalid user/password ... try again'
            self.email, self.password = request_id()

        session.quit()

    def get_data(self):
        self.receiver = raw_input('To >> ')
        self.body = request_list()

    def send_message(self):
        session = open_session(self.server, self.port)
        session.login(self.email, self.password)
        
        headers = [
                "From: " + self.email,
                "Subject: Shopping List" ,
                "To: " + self.receiver,
                "Content-Type: text/plain"
                ]
        headers = "\r\n".join(headers)

        # sendmail( sender, receiver, message)
        session.sendmail(
                self.email,
                self.receiver,
                headers + "\r\n\r\n" + self.body
                )
        session.quit()

    def set_alarm(self):
        now = datetime.now()
         # The input should be something like this 18:45
        timer = raw_input('Set alarm, 24Hrs format >> ')
        timer = map(int,re.split(":",timer))

        delta = (timer[0] - now.hour )*3600 + (timer[1] - now.minute)*60 

        s = sched.scheduler(time.time, time.sleep)
        s.enter(delta, 1, self.send_message,())
        s.run()

######################################
#      M A I N
######################################

gm = Gmail_api()
gm.get_data()
gm.set_alarm()

