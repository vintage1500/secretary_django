from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
PROVIDER_TOKEN = ""
ADMINS = ''

DB_NAME = 'secretary_faculty'
DB_HOST = 'localhost'
DB_PASSWORD = '12345678'
DB_PORT = ''
DB_USER = 'postgres'


