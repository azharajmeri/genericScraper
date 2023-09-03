import os

from dotenv import load_dotenv

load_dotenv()

# Database settings
DB_CONFIG = {
    "host": os.environ.get("DATABASE_HOST"),
    "user": os.environ.get("DATABASE_USER"),
    "password": os.environ.get("DATABASE_PASSWORD"),
    "database": os.environ.get("DATABASE_NAME")
}
