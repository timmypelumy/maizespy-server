from app.config.settings import get_settings
from .main import huey
from app.database import sync_db as db, Collections
from app.utils.helpers import predict_images
from app.models.predictor import PredictionResult, ResultItem
from app.models.enums import LabelClasses

settings = get_settings()


@huey.task(retries=1 , retry_delay=20, name = "task_predict_images")
def task_predict_images( data :  list[dict] ):
    
    predictions = predict_images(data)

    entries = []

    for x in data:

        r = PredictionResult(request_id = x["prediction_request_id"], result = ResultItem(id = x["image_id"], label_class = LabelClasses.BLIGHT) )
        
        entries.append(r.model_dump())

    db[Collections.prediction_results].insert_many(entries)

    print( "Predictions: ", entries)



