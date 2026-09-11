import os
from dotenv import load_dotenv

load_dotenv()

class settings:
    origins = os.getenv("ORIGINS")
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")

settings = settings()

# In main.py
# from config import settings
# origin = setting.origins

