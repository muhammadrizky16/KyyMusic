##Config

from os import getenv
from dotenv import load_dotenv

load_dotenv()
get_queue = {}
SESSION_NAME = getenv('SESSION_NAME', 'BQDDH59bBiUaKYBkAycoDZp3c1BTcu5tGlyJjkbLfdK4M-HbkNrSHhb6YkNX6HDpn1ny_PW82f2UvsqAzwzSAEtBcWnfEJ1B0xzycZksad0-AoMrI75qMYaSjV3RUPdmJNLMNPrs68gMCV4-enuYq-m4AW33FEPRbTEz0YQ7LgXr-Yo4A8RD9-ItXMseDluJ6Fzi2oYmvd1F_8RLN-DkFkghgXRZJU3Bb2uUH1IyHvamEdzw5yVLeWYUlz4qZ3sXTG0NolYExPRMRSETK38pDO56azeUrlCDxCJmgStxgONiprJ1uzgegl9640OxyYM0wJYsHV-vJpsX89fj26BJirrsAAAAAU9dcc8A')
BOT_TOKEN = getenv('BOT_TOKEN', '5688006568:AAEtZqURbEmqm2ZMqWxe_r3SeqodD5DJ56w')
API_ID = int(getenv('API_ID', "19906979"))
API_HASH = getenv('API_HASH', '651189e1f7801f9577c0d9e0c3386fed')
DURATION_LIMIT = int(getenv('DURATION_LIMIT', '3600'))
COMMAND_PREFIXES = list(getenv('COMMAND_PREFIXES', '/ . , : ; !').split())
MONGO_DB_URI = getenv("mongodb+srv://yudiae75:123@mv.enzforp.mongodb.net/?retryWrites=true&w=majority")
SUDO_USERS = list(map(int, getenv('SUDO_USERS', '2092091491').split()))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", '-1001774721571'))
ASS_ID = int(getenv("ASS_ID", '18625854'))
OWNER_ID = list(map(int, getenv('OWNER_ID', '19906979').split()))
GROUP = getenv("GROUP", 'mvRumahSinggah')
CHANNEL = getenv("CHANNEL", 'Jejakhariini')
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/wahyu-123/Music")
AUTO_LEAVE = int(getenv("AUTO_LEAVE", "1500"))
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

# KALO FORK/CLONE JAN DI HAPUS KENTOD
OWNER_ID.append(19906979)
OWNER_ID.append(18625854)
