from dotenv import load_dotenv
import os


load_dotenv()

class Config:
    """Base config class."""
    APIKEY = os.environ.get('APIKEY')