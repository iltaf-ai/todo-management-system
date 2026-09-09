import os
from dotenv import load_dotenv

load_dotenv()

class settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_EXPIRE_TOKEN_TIME = int(
        os.getenv("ACCESS_EXPIRE_TOKEN_TIME", "30")
    )
    SQL_URL = os.getenv("SQL_URL")

settings = settings()