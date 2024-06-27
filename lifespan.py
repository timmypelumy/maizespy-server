from fastapi import FastAPI
from tensorflow.keras.models import load_model
import asyncio
from contextlib import asynccontextmanager


model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model

    try:

        # Load the ML model
        # model = await asyncio.to_thread(load_model, "./app/maizespy.keras")
        model = load_model("./app/maizespy.keras")
        print("Model loaded successfully")
        yield
        # Clean up the ML models and release the resources
        model = None

    except Exception as e:
        print("Error loading model: ", e)
        yield
        model = None