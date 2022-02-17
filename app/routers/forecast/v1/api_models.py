"""Defines request and response data models"""
from datetime import datetime
from typing import List

from pydantic import Field

from app.core.base_model import BaseModel
from app.models.v1.shared_models import (
    InputdataModel,
    PredictionJobModel,
    QuantileModel,
)


# REQUEST MODELS #######################################################################
class ForecastRequestModel(BaseModel):
    """Forecast Request Model"""

    prediction_job: PredictionJobModel
    input_data: InputdataModel


# RESPONSE MODELS ######################################################################
class ForecastResponseModel(BaseModel):
    """Forecast Response Model"""

    index: List[datetime] = Field(
        ...,
        description="Datetime index of forecast",
        example=[
            "2021-04-30T14:00:00.000Z",
            "2021-04-30T14:15:00.000Z",
            "2021-04-30T14:30:00.000Z",
        ],
    )
    forecast: List[float] = Field(
        ...,
        description="The forecasted load",
        example=[-4.966667, -5.206667, -5.652781],
    )
    stdev: List[float] = Field(..., description="Standard deviation of the forecast")
    quantiles: List[QuantileModel] = Field(..., description="")
