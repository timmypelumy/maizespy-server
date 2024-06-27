from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings
from app.routes.predictor import router as predict_router
from app.huey_tasks.main import huey


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,

)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(predict_router, prefix="/api/predictor", tags=["Predictor"])
