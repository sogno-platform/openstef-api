"""Defines request and response data models"""
from typing import List
from pydantic import Field

from app.models.v1.shared_models import InputdataModel, PredictionJobModel
from app.core.base_model import BaseModel


# REQUEST MODELS #######################################################################
class OptimizeHyperparametersRequestModel(BaseModel):
    """Hyperparameters request model"""
    prediction_job: PredictionJobModel
    input_data: InputdataModel
    horizons: List[float] = Field([0.25, 24], description="Training horizons")
    n_trials: int = Field(8, description="Number of trials")
    timeout: int = Field(600, description="Optimization timeout in seconds")


# RESPONSE MODELS ######################################################################
class OptimizeHyperparametersResponseModel(BaseModel):
    """Optimize hyperparameters response model.
    """
    task_id: str = Field(
        ..., description="Optimize hyperparameters task id"
    )
    status_url: str = Field(..., description="Optimize hyperparameters status url")