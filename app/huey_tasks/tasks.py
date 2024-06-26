from pymongo import MongoClient
from pydantic import EmailStr
from huey.exceptions import CancelExecution
from huey import crontab
from app.config.settings import get_settings
from .main import huey
from app.utils.helpers import get_utc_timestamp


settings = get_settings()

client = MongoClient(settings.db_url)

db = client[settings.db_name]


# Task to test the huey consumer
@huey.task(retries=3,  retry_delay=10, name="task_system_check")
def task_test_huey():

    if not settings.debug:
        raise CancelExecution(retry=False)

    db["task_queue"].insert_one({"ts": get_utc_timestamp()})
    return
