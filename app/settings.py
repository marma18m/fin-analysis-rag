import os 
from dotenv import load_dotenv
load_dotenv()

class Settings:
    """
    Settings for the application.
    """
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    qdrant_url: str = os.getenv("QDRANT_URL")
