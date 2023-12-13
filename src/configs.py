import os


# Local

# https://www.coingecko.com/api/documentation
CG_API_KEY = os.getenv("CG_API_KEY", "")
# https://russianinvestments.github.io/investAPI/token/
TINKOFF_API_KEY = os.getenv("TINKOFF_API_KEY", "")

# Base

TEMP_DIRECTORY_NAME = "temp"
LOG_FILE_NAME = "app.log"
