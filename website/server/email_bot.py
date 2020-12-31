import smtplib as smt
from email.message import EmailMessage
import ssl

class EmailBot():
    """
    A email_bot to send emails. Configured to use Gmail account.

    Attributes:
        sender : Email-id to send the email from
        password : Password of the sender email
        
    TODO Add comment for email setup process to use the bot.
         Add support for other account types.
         Add exception handling.
                
    
    """
    sender : str
    password : str


    def __init__(self, sender:str, password:str) -> None:
        """
        Initiates the bot with proper email account.
        :param sender: 
        :param password: 
        """
        self.sender = sender
        self.password = password
        # self.context = ssl.create_default_context()
        # try:
        #     self.server = smt.SMTP("smtp.gmail.com", 587)
        #     self.server.ehlo()
        #     self.server.starttls()
        #     self.server.login(self.sender, self.password)
        #     # self.server.sendmail(FROM, TO, message)
        #     # self.server.close()
        #     print('successfully sent the mail')
        # except Exception:
        #     print("failed to send mail")
        # # try:
        # #     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # #     server.ehlo()
        # #     server.login(self.sender,self.password)
        # try:
        #     self.smtp = smt.SMTP()
        #     self.smtp.connect('smtp.gmail.com', '587')
        #     self.smtp.ehlo()
        #     self.smtp.starttls(context=self.context)
        #     self.smtp.login(self.sender,self.password)
        # except Exception:
        #     print('something went wrong when making email bot.')

    @staticmethod
    def sendmail(receiver:str, subject:str, body:str) -> bool:
        """
        Send a email to the receiver with given subject and body text.
        :param receiver: email id of the receiver.
        :param subject: subject of the email.
        :param body: body of the email.
        :return: returns true if the email was sent successfully and 
                false otherwise.
        """
        sender = 'robotics@utmsu.ca'
        password = 'autonomousenthusiasts'
        message = 'Subject: {}\n\n{}'.format(subject, body)
        context = ssl.create_default_context()
        print(receiver)
        print(message)
        with smt.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
                # server = smt.SMTP("smtp.gmail.com", 587)
                # server.starttls()
                server.login(sender, password)
                server.ehlo()
                server.sendmail(sender, receiver, message)
                # server.close()
                print('successfully sent the mail')
                return True
            except Exception:
                print("failed to send mail")
                return False
