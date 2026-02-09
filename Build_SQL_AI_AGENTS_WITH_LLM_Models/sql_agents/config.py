import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "sqlite:///sample.db")
    
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set. Please check your .env file.")

config = Config()
