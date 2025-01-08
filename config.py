import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')
API_URL = os.getenv('API_URL')
PORT = int(os.getenv('PORT')) # 不转报错
REFERENCE_ID = os.getenv('REFERENCE_ID')
