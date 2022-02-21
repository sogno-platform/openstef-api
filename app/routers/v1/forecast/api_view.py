"""Defines API endpoints. Uses `controller.py` to handle the actual logic"""
import structlog
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.exceptions import ModelNotFoundError
from app.schemas.v1.shared_models import ForecastType
from app.routers.v1.forecast.api_models import (
    ForecastRequestModel,
    ForecastResponseModel,
)
from app.routers.v1.forecast.controller import ForecastController

router = APIRouter()

controller = ForecastController()

logger = structlog.get_logger(__name__)


@router.post("/generate", response_model=ForecastResponseModel)
async def generate_forecast(forecast_request: ForecastRequestModel):
    """Generate a forecast.
    For an input example, see data/*generate_forecast_input*.json

    Returns:
        ForecastResponseModel.
    """

    if forecast_request.prediction_job.forecast_type is ForecastType.BASECASE:
        return controller.generate_basecase_forecast(forecast_request)

    try:
        return controller.generate_forecast(forecast_request)
    except ModelNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No model found for generating this forecast",
        )
