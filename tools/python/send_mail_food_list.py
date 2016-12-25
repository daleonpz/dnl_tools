#!/usr/bin/python2.7

import smtplib
import getpass

class Gmail_api(object):
    def __init__(self, email, password):
        self.email = email + "@gmail.com"
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
        
        session = smtplib.SMTP(self.server, self.port)
        session.ehlo() #Identify yourself to the server. 
        session.starttls() # Transport layer security
        session.login(self.email, self.password)

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

mail = raw_input('gmail user >> ')
password = getpass.getpass('password >> ')
receiver = raw_input('To >> ')

gm = Gmail_api(mail, password)
gm.send_message(receiver, 'To buy', 'This is the body')

