import smtplib, ssl
from ..config import Configuration


class EmailBot:
    def __init__(self):
        self.port = 465

    def __enter__(self):
        self.sender = Configuration.FROM_EMAIL_ADDR
        self.password = Configuration.FROM_EMAIL_PASS
        sekf.context = ssl.create_default_context()
        return self

    def __exit__(self, type, value, tb):
        pass

    def send_register(self):
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as email:
            email.login(self.sender, self.password)
            email.sendmail(sender, 'aalex.lin@mail.utoronto.ca', message)