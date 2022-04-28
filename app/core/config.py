import os

from dotenv import load_dotenv

load_dotenv("./.env")


API_USERNAME = os.environ["API_USERNAME"]
API_PASSWORD = os.environ["API_PASSWORD"]

# Auth configs.

#API_SECRET_KEY = os.environ["API_SECRET_KEY"]
API_ALGORITHM = os.environ["API_ALGORITHM"]

API_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["API_ACCESS_TOKEN_EXPIRE_MINUTES"])  # infinity

API_AUTH_CFG = os.environ["API_AUTH_CFG"]

IMG_SAVE_DIR = os.environ["IMG_SAVE_DIR"]

IMG_CACHE_DIR = os.environ["IMG_CACHE_DIR"]

DEBUG = bool(int(os.environ["DEBUG"]))

JWT_KEY_DIR = os.environ["JWT_KEY_DIR"]

JWT_KEY_NAME = os.environ["JWT_KEY_NAME"]

MAX_IMG_SIZE = int(os.environ["MAX_IMG_SIZE"]) or 999999999999 # No limit if set to zero.

RETURN_SAVEFP = bool(int(os.environ["RETURN_SAVEFP"]))

ENFORCE_TOKEN_IP = bool(int(os.environ["ENFORCE_TOKEN_IP"]))