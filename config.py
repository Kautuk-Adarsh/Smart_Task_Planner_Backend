import os
import logging
from dotenv import load_dotenv
from google import genai

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-task-planner")

API_KEY = os.getenv("PROJECT_API_KEY")

if not API_KEY:
    logger.error("PROJECT_API_KEY not found in environment variables.")
    raise ValueError("PROJECT_API_KEY environment variable is required.")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_URI or not MONGO_DB_NAME:
    logger.error("MONGO_URI or MONGO_DB_NAME not found in environment variables.")


def initialize_gemini_client():
    """Initializes the synchronous Gemini client using the API key."""
    try:
        client = genai.Client(api_key=API_KEY)
        return client
    except Exception as e:
        logger.error("Error initializing Gemini client: %s", e)
        raise RuntimeError("Failed to initialize Gemini Client.") from e
