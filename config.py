from dotenv import load_dotenv
load_dotenv()
import os

API_URL = 'https://paper-api.alpaca.markets'
API_KEY = os.environ.get("api_key")
API_SECRET = os.environ.get("api_secret")

DB_HOST = os.environ.get("db_host")
DB_USER = os.environ.get("db_user")
DB_PASS = os.environ.get("db_password")
DB_NAME = os.environ.get("db_name")
DB_PORT = os.environ.get("db_port")
