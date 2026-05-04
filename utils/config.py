import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

def get_db_config(db_mode="local"):
    if db_mode == "local":
        return {
            "host": os.getenv("DB_LOCAL_HOST"),
            "user": os.getenv("DB_LOCAL_USER"),
            "password": os.getenv("DB_LOCAL_PASS"),
            "database": os.getenv("DB_LOCAL_NAME"),
            "port":os.getenv("DB_LOCAL_PORT")
        }
    elif db_mode == "remote":
        return {
            "host": os.getenv("DB_REMOTE_HOST"),
            "user": os.getenv("DB_REMOTE_USER"),
            "password": os.getenv("DB_REMOTE_PASS"),
            "database": os.getenv("DB_REMOTE_NAME"),
            "port":os.getenv("DB_REMOTE_PORT")
        }
    else:
        raise ValueError("Unknown DB mode")