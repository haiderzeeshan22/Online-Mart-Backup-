from  starlette.config import Config
from starlette.datastructures import Secret



try:
    config = Config(".env")

except FileNotFoundError:
    config = Config()

USERDB_URL = config("USERDB_URL", cast=Secret)        