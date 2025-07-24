from pathlib import Path

from dotenv import load_dotenv

# Loading env variables from .env file
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
