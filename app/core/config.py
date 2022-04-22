import os

from dotenv import load_dotenv
from databases import DatabaseURL
from starlette.datastructures import CommaSeparatedStrings

API_V1_STR = "/api"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 * 4 # one month

load_dotenv(".env")

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "")
    MONGO_DB = os.getenv("MONGO_DB", "aligner")

    MONGODB_URL = DatabaseURL(
        f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    )
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)
    MONGO_DB = os.getenv("MONGO_DB", "aligner")

db_name = MONGO_DB
accounts_collection_name = "accounts"
datasets_collection_name = 'datasets'
sentence_pairs_collection_name = "sentence_pairs"


SECRET_KEY = os.getenv("SECRET_KEY", "local_secret_key")
