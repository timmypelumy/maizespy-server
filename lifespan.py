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
        model = load_model("./app/maizespy.keras")
        print("Model loaded successfully")
        yield

    except Exception as e:
        print("Error loading model: ", e)
        yield

    finally:
        # Clean up the ML models and release the resources
        model = None
        print("Model cleaned up")