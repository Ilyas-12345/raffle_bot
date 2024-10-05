from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.environ.get('TOKEN')
URL_RAFFLE_CONDITION = os.environ.get('URL_RAFFLE_CONDITION')
URL_RAFFLE_PERSONAL_DATA_PROCESSING = os.environ.get('URL_RAFFLE_PERSONAL_DATA_PROCESSING')

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
JWT_TOKEN = os.environ.get("JWT_TOKEN")

