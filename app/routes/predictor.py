from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from .utils import predict_single_image
import numpy as np
import os
import shutil


router = APIRouter()
