"""Defines request and response data models"""
from datetime import datetime
from app.core.base_model import BaseModel


# RESPONSE MODELS ######################################################################
class OptimizeHyperparametersTaskResponseModel(BaseModel):
    id: str
    optimize_done: bool
    created: datetime
    duration: int
    prediction_job_id: int
    optimize_failed: bool
    reason_failed: str
