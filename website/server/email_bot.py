import smtplib as smt

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
        self.smtp = smt.SMTP('smtp.gmail.com',587)
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.ehlo()
        self.smtp.login(self.sender,self.password)

    def sendmail(self,receiver:str, subject:str, body:str) -> bool:
        """
        Send a email to the receiver with given subject and body text.
        :param receiver: email id of the receiver.
        :param subject: subject of the email.
        :param body: body of the email.
        :return: returns true if the email was sent successfully and 
                false otherwise.
        """
        message = 'Subject: {}\n\n{}'.format(subject, body)
        self.smtp.sendmail(self.sender, receiver, message)
