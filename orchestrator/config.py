from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("AICORE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AICORE_CLIENT_SECRET")
TOKEN_URL = os.getenv("AICORE_TOKEN_URL")
AI_CORE_BASE_URL = os.getenv("AICORE_BASE_URL")
