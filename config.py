import os
import urllib.parse
class Config:
    senha = urllib.parse.quote_plus("senai@123")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"mysql+pymysql://root:{senha}@localhost/saas_platform")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

