from tensorflow.keras.preprocessing import image
from app.utils.helpers import load_model_silently
from fastapi import UploadFile
import numpy as np
import os
import shutil


model_path  =  "./app/maizespy.keras"

model = load_model_silently(model_path)

target_size = (256, 256)

# Function to preprocess and predict on a single image array
def predict_single_image(img_array):
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)  
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    return predicted_class_index




def predict_images( files :  list[UploadFile]):

    predictions = []

    for file in files:
        # Save to temp location

        file_location = f"./temp/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load and preprocess 
        img = image.load_img(file_location, target_size=target_size)
        img_array = image.img_to_array(img)

        # Make prediction 
        predicted_class_index = predict_single_image(img_array)

        # Append prediction result
        predictions.append({
            "filename": file.filename,
            "predicted_class_index": predicted_class_index
        })

        # Remove the temporary file
        os.remove(file_location)

    return predictions