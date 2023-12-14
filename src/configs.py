import os


# Local

CG_API_KEY = os.getenv("CG_API_KEY", "")  # https://www.coingecko.com/api/documentation
TINKOFF_API_KEY = os.getenv(
    "TINKOFF_API_KEY", ""
)  # https://russianinvestments.github.io/investAPI/token/
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")

POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Base

TEMP_DIRECTORY_NAME = "temp"
LOG_FILE_NAME = "app.log"
