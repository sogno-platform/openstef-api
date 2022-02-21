"""Define an API version by making a selection of API routers"""

from fastapi import FastAPI

from app.core.settings import Settings
from app.routers.v1.forecast.api_view import router as forecast_router
from app.routers.v1.hyperparameters.api_view import router as hyperparameters_router
from app.routers.v1.optimize_hyperparameters_task.api_view import (
    router as optimize_hyperparameters_task_router,
)
from app.routers.v1.trained_model.api_view import router as trained_model_router
from app.routers.v1.trained_model_task.api_view import router as train_model_task_router

app = FastAPI(
    title=Settings.app_name,
    description=Settings.app_description,
    version="v1",
    root_path="/api/v1",
)

app.include_router(forecast_router, prefix="/forecasts", tags=["forecasts"])
app.include_router(
    hyperparameters_router, prefix="/hyperparameters", tags=["hyperparameters"]
)
app.include_router(
    optimize_hyperparameters_task_router,
    prefix="/optimize-hyperparameters-tasks",
    tags=["optimize-hyperparameters-tasks"],
)
app.include_router(
    trained_model_router, prefix="/trained-models", tags=["trained-models"]
)
app.include_router(
    train_model_task_router, prefix="/train-model-tasks", tags=["train-model-tasks"],
)
