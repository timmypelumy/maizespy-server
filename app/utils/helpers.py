import os
from uuid import uuid4
from fastapi import HTTPException
from datetime import datetime, timezone
from fastapi import status as status_codes
from app.config.settings import get_settings
from tensorflow.keras.preprocessing import image
import requests
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from lifespan import model



settings = get_settings()

target_size = (256, 256)


def make_url(frag, surfix="", base_url=""):

    if not base_url:
        return "{0}{1}".format(frag, surfix)

    return "{0}{1}{2}".format(base_url, frag, surfix)




# Function to preprocess and predict on a single image array
def predict_single_image(img_array):
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)  
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    return predicted_class_index




def predict_images( images : list[dict]):

    if model is None:
        raise ValueError("Model is not loaded")

    predictions = []

    for item in images:

        image_str  =  item["image_str"]

        image_data = base64.b64decode(image_str)
        img = Image.open(BytesIO(image_data))
        
        img_array = image.img_to_array(img.resize(target_size))

        # Make prediction 
        predicted_class_index = predict_single_image(img_array)

        # Append prediction result
        predictions.append({
            "predicted_class_index": predicted_class_index,
            "image_id" : item["image_id"],
            "prediction_request_id" : item["prediction_request_id"]
        })

    return predictions


def make_request(url, method, headers={}, body=None):
    _headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    _headers.update(headers)

    response = requests.request(
        method=method, url=url, headers=_headers, json=body)

    status = response.status_code
    ok = response.ok

    if not ok:

        return ok, status, None

    data = response.json()

    return ok, status, data


def handle_response(ok, status, data, silent=True):
    if not ok:

        if not silent:
            raise HTTPException(400)

    if not (status >= status_codes.HTTP_200_OK and status < status_codes.HTTP_300_MULTIPLE_CHOICES):

        if not silent:
            raise HTTPException(400)

        return False

    if status == status_codes.HTTP_401_UNAUTHORIZED:

        if not silent:
            raise HTTPException(400)

        return False

    return True


def get_uuid4():
    return str(uuid4().hex)


def get_random_string(length: int = 32):
    return os.urandom(length).hex()


def get_utc_timestamp() -> float:
    return datetime.now(tz=timezone.utc).timestamp()


def get_id(n=12):
    return os.urandom(n).hex()
