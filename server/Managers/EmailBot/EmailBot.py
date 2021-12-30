import os, smtplib, ssl
from email.message import EmailMessage

from server.config import Configuration

Email_Titles = {'registration': 'Welcome to Deerhunt!'}


class EmailBot:
    def __init__(self):
        self.port = 465

    def __enter__(self):
        self.sender = Configuration.FROM_EMAIL_ADDR
        self.password = Configuration.FROM_EMAIL_PASS
        self.context = ssl.create_default_context()
        return self

    def __exit__(self, type, value, tb):
        pass

    def build_message_registration(self, code) -> None:
        """
        Opens registration.html, reads contents and builds
        email message with unique verification link.
        """
        with open('Managers/EmailBot/{}.html'.format('registration')) as file:
            self.msg = EmailMessage()
            self.msg.set_content(file.read().replace('{{ Registeration_link }}',
                                                     f'http://{Configuration.FLASK_ADDR}/api/user/verify/{code}'),
                                 subtype='html')
        self.msg['Subject'] = Email_Titles['registration']
        self.msg['From'] = self.sender

    def build_message_forgotpassword(self, code) -> None:
        """
        Opens forgotpassword.html, reads contents and builds
        email message with unique verification link.
        """
        with open('Managers/EmailBot/{}.html'.format('forgotpassword')) as file:
            self.msg = EmailMessage()
            self.msg.set_content(
                file.read().replace('{{ Password_Reset_link }}',
                                    f'http://{Configuration.FLASK_ADDR}/api/user/forgotpassword/{code}'),
                subtype='html')
        self.msg['Subject'] = Email_Titles['registration']
        self.msg['From'] = self.sender

    def send(self, receiver) -> None:
        """
        Sends email message.
        """
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port,
                              context=self.context) as email:
            try:
                email.login(self.sender, self.password)
                self.msg['To'] = receiver
                email.send_message(self.msg)
            except smtplib.SMTPException as e:
                print('email could not be sent')
                print(e)

    def check_login(self):
        """
        Checks if email bot is logged in.
        """
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port) as email:
            try:
                email.login(self.sender, self.password)
            except smtplib.SMTPException as e:
                print('email can not be logged in')
                print(e)


with EmailBot() as e:
    e.check_login()
