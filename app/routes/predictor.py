from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from .util import predict_single_image
from app.models.predictor import *
from app.database import db, Collections
import numpy as np
import os
import shutil

router = APIRouter()


@router.post("/predict", response_model= list[PredictionRequest])
async def predict_maize_disease(images: list[ImageData]):

    prediction_request = PredictionRequest(image_count =  len(images))

    await db[Collections.prediction_requests].insert_one(prediction_request.model_dump())

    return prediction_request


