import smtplib, ssl
from email.message import EmailMessage
import os
from ..config import Configuration


Email_Titles = {'registration': 'Welcome to Deerhunt!'}


class EmailBot:
    def __init__(self, purpose=None):
        self.purpose = purpose
        self.port = 465

    def __enter__(self):
        self.sender = Configuration.FROM_EMAIL_ADDR
        self.password = Configuration.FROM_EMAIL_PASS
        self.context = ssl.create_default_context()
        self.build_message()
        return self

    def __exit__(self, type, value, tb):
        pass

    def build_message(self):
        with open('EmailBot/{}.html'.format(self.purpose)) as file:
            self.msg = EmailMessage()
            self.msg.set_content(file.read(), subtype='html')
        self.msg['Subject'] = Email_Titles[self.purpose]
        self.msg['From'] = self.sender

    def send(self, receiver):
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as email:
            email.login(self.sender, self.password)
            self.msg['To'] = '{}@mail.utoronto.ca'.format(receiver)
            email.send_message(self.msg)
