import os

class Configuration:
    MONGODB_URI = os.getenv('MONGODB_URI')
    FROM_EMAIL_ADDR = os.getenv('FROM_EMAIL_ADDR')
    FROM_EMAIL_PASS = os.getenv('FROM_EMAIL_PASS')