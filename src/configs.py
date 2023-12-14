import os


# Local

CG_API_KEY = os.getenv("CG_API_KEY", "")  # https://www.coingecko.com/api/documentation
TINKOFF_API_KEY = os.getenv(
    "TINKOFF_API_KEY", ""
)  # https://russianinvestments.github.io/investAPI/token/
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")

# Base

TEMP_DIRECTORY_NAME = "temp"
LOG_FILE_NAME = "app.log"
