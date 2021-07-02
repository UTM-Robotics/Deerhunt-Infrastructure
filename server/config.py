import os
from dotenv import load_dotenv
from .Database.mongodb import DatabaseManager

load_dotenv()

class Configuration:
    MONGODB_URI = os.getenv('MONGODB_URI')
    FLASK_ADDR = os.getenv('FLASK_ADDR')
    FROM_EMAIL_ADDR = os.getenv('FROM_EMAIL_ADDR')
    FROM_EMAIL_PASS = os.getenv('FROM_EMAIL_PASS')
    MAIL_DOMAINS = os.getenv("MAIL_DOMAINS").split()
    # Mongo = DatabaseManager.init_database(MONGODB_URI)
