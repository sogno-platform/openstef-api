"""Define an API version by making a selection of API routers"""

from fastapi import FastAPI

from app.core.settings import Settings
from app.routers.v2.models.model_api import router as model_router
from app.routers.v2.training.training_api import router as training_router
from app.routers.v2.prediction.prediction_api import router as prediction_router

app = FastAPI(
    title=Settings.app_name,
    description=Settings.app_description,
    version="v2",
    root_path="/api/v2",
)

app.include_router(model_router, prefix="/model", tags=["Model"])
app.include_router(
    training_router, prefix="/training", tags=["Training"]
)
app.include_router(
    prediction_router,
    prefix="/prediction",
    tags=["Prediction"],
)