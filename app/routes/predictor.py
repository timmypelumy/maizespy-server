from fastapi import APIRouter
from app.models.predictor import *
from app.database import db, Collections
from app.huey_tasks.tasks import task_predict_images


router = APIRouter()


@router.post("/predict", response_model= list[PredictionRequest])
async def predict_maize_disease(images: list[ImageData]):

    entries = []

    task_data = []

    for image_data in images:

        r = PredictionRequest(image_id = image_data.id )

        entries.append( r.model_dump())

        task_data.append({
            "prediction_request_id" : r.uid,
            "file" : image_data.image,
            "image_id" : image_data.id
        })


    await db[Collections.prediction_requests].insert_many(entries)


    task_predict_images(task_data)


    return entries



