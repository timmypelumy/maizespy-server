from app.config.settings import get_settings
from .main import huey
from app.database import sync_db as db, Collections
from app.utils.helpers import predict_images
from app.models.predictor import PredictionResult, ResultItem
from datetime import timedelta
from tensorflow.keras.models import load_model


settings = get_settings()

model = None


try:
    model = load_model(settings.ml_model_path)
    print("Model loaded successfully")
except Exception as e:
    raise Exception("Error loading model: ", e)


@huey.task(retries=1, retry_delay=20, name="task_predict_images", expires=timedelta(minutes=5))
def task_predict_images(data:  list[dict]):

    predictions = predict_images(model, data)

    entries = []

    for x in predictions:

        r = PredictionResult(prediction_request_id=x["prediction_request_id"], result=ResultItem(
            image_id=x["image_id"], label_class=x["label"]))

        entries.append(r.model_dump())

    db[Collections.prediction_results].insert_many(entries)

    if settings.debug:

        print("Predictions: ", predictions)
