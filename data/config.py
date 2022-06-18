import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
PGUSER = str(os.getenv("POSTGRES_USER"))
PGPASSWORD = str(os.getenv("POSTGRES_PASSWORD"))
DATABASE = str(os.getenv("DB_NAME"))

REDIS_HOST = str(os.getenv("REDIS_HOST", default="localhost"))
REDIS_PORT = int(os.getenv("REDIS_PORT", default=6379))
REDIS_DB_FSM = int(os.getenv("REDIS_DB_FSM", default=0))
REDIS_DB_JOBSTORE = int(os.getenv("REDIS_DB_JOBSTORE", default=1))
REDIS_DB_JOIN_LIST = int(os.getenv("REDIS_DB_JOIN_LIST", default=2))


admins = [
    417804053
]

ip = os.getenv("ip")


POSTGRES_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}"
