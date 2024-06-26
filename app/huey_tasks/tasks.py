from pymongo import MongoClient
from pydantic import EmailStr
from huey.exceptions import CancelExecution
from huey import crontab
from app.config.settings import get_settings
from .main import huey
from app.utils.helpers import get_utc_timestamp
from app.database import sync_db as db, Collections
from app.utils.helpers import predict_images
from app.models.predictor import PredictionResult, ResultItem
from app.models.enums import LabelClasses

settings = get_settings()


@huey.task(retries=1 , retry_delay=20, name = "task_predict_images")
def task_predict_images( data :  list[dict] ):

    image_files = [ d["file"] for d in data ]
    
    predictions = predict_images(image_files)

    entries = []

    for x in data:

        r = PredictionResult(request_id = x["prediction_request_id"], result = ResultItem(id = x["image_id"], label_class = LabelClasses.BLIGHT) )
        
        entries.append(r.model_dump())

    db[Collections.prediction_results].insert_many(entries)

    print(predictions)



# Task to test the huey consumer
@huey.task(retries=3,  retry_delay=10, name="task_system_check")
def task_test_huey():

    if not settings.debug:
        raise CancelExecution(retry=False)

    db["task_queue"].insert_one({"ts": get_utc_timestamp()})
    return
