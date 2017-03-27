#!/usr/bin/python2.7

############################
#  TO DO
############################
# - read from org-mode file / txt file
import smtplib
import getpass
import re
import time, sched
import markdown
import codecs

from datetime import timedelta, datetime

###################################
#   F u n c t i o n s
###################################
def request_id():
    mail = raw_input('gmail user >> ')
    password = getpass.getpass('password >> ')

    return mail + '@gmail.com', password

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

    def set_body(self, body):
        self.body = body

    def get_mddata(self, path):
        f = open(path,'r')
        md = f.read()
        self.body = markdown.markdown(md)
        f.close()
    
    def get_mddata_utf8(self, path):
        f = codecs.open(path,mode='r', encoding="utf-8")
        md = f.read()
        self.body = markdown.markdown(md)
        f.close()
    
    def set_headers(self, subject, receiver, ct_type):
        self.subject = subject
        self.receiver = receiver
        self.ct_type = ct_type


    def send_message(self):
        session = open_session(self.server, self.port)
        session.login(self.email, self.password)
        
        headers = [
                "From: " + self.email,
                "Subject: " + self.subject ,
                "To: " + self.receiver,
                "Content-Type: text/" + self.ct_type,
                ]
        headers = "\r\n".join(headers)

        # sendmail( sender, receiver, message)
        session.sendmail(
                self.email,
                self.receiver,
                headers + "\r\n\r\n" + self.body.encode('utf-8')
                )
        session.quit()

    def set_alarm(self, giventime):
        now = datetime.now()
         # The input should be something like this 18:45
        timer = map(int,re.split(":",giventime))

        delta = (timer[0] - now.hour )*3600 + (timer[1] - now.minute)*60 

        s = sched.scheduler(time.time, time.sleep)
        s.enter(delta, 1, self.send_message,())
        s.run()

######################################
#      M A I N
######################################

