from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings
from app.routes.predictor import router as predict_router
from app.huey_tasks.main import huey
from tensorflow.keras.models import load_model
import asyncio
from contextlib import asynccontextmanager

settings = get_settings()

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



app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan = lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(predict_router, prefix="/api/predictor", tags=["Predictor"])
