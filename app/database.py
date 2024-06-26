from motor import motor_asyncio
from app.config.settings import get_settings
from pymongo import MongoClient
from enum import Enum

settings = get_settings()

client = MongoClient(settings.db_url)

sync_db = client[settings.db_name]


class Collections(str, Enum):
    users = "Users"


client = motor_asyncio.AsyncIOMotorClient(settings.db_url)


db = client[settings.db_name]
