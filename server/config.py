import os
from dotenv import load_dotenv

load_dotenv()

class Configuration:

    # Saving flask specific env
    ENV = os.getenv('FLASK_ENV')
    TESTING = os.getenv('TESTING')

    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGODB_URI = os.getenv('MONGODB_URI')
    FLASK_ADDR = os.getenv('FLASK_ADDR')
    FROM_EMAIL_ADDR = os.getenv('FROM_EMAIL_ADDR')
    FROM_EMAIL_PASS = os.getenv('FROM_EMAIL_PASS')
    MAIL_DOMAINS = os.getenv("MAIL_DOMAINS").split()
    ADMIN_USERNAME=os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD")
    AZURE_KEY = os.getenv("AZURE_KEY")
    
