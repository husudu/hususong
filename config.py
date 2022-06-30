import os
API_ID = 1425632
API_HASH = "e5861d507c3c2a73a354a3c12f8141f8"
BOT_TOKEN = "5514356101:AAHW-06CGkjrwM8ZBTbKtimjH7LUbHp2FiQ"
DATABASE_URL = os.getenv("DATABASE_URL")
OWNER_ID = list({int(x) for x in os.environ.get("OWNER_ID", "").split()})
