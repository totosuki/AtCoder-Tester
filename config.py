from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("username")
PASSWORD = os.getenv("password")
PATH = os.getenv("path")