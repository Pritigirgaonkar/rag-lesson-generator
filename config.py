import os
from dotenv import load_dotenv

load_dotenv()

MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MAX_RETRIES = max(0, min(int(os.getenv("MAX_RETRIES", "2")), 2))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
