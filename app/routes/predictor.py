from fastapi import APIRouter
from app.models.predictor import *
from app.database import db, Collections
from app.huey_tasks.tasks import task_predict_images


router = APIRouter()


@router.post("/results", response_model=list[PredictionResult])
async def get_prediction_results(prediction_requests_ids:  list[str]):

    query = {"prediction_request_id": {"$in": prediction_requests_ids}}

    cursor = db[Collections.prediction_results].find(query)

    items = [PredictionResult(**x) for x in await cursor.to_list(length=None)]

    return items


@router.post("/predict", response_model=list[PredictionRequest])
async def predict_maize_disease(images: list[ImageData]):

    entries = []

    task_data = []

    for image_data in images:

        r = PredictionRequest(image_id=image_data.id)

        entries.append(r.model_dump())

        task_data.append({
            "prediction_request_id": r.uid,
            "image_str": image_data.image_string,
            "image_id": image_data.id
        })

    if len(entries) > 0:
        await db[Collections.prediction_requests].insert_many(entries)

        task_predict_images(task_data)

    return entries
