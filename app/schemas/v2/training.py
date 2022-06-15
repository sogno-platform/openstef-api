from __future__ import annotations
from typing import Optional, Dict, Any, Union
from proloaf.modelhandler import TrainingRun
from app.core.base_model import BaseModel


from pydantic import Field
from .data import InputData
from .job import Job
from .model import PredModelBase

# Training
class TrainingBase(BaseModel):
    data: InputData
    max_training_time: Optional[int] = Field(
        None, ge=0, description="Maximum training duration in seconds"
    )
    model: Union[
        int, PredModelBase
    ] = Field(  # TODO should be possible to be a full (with id) predModel for the result.
        ...,
        description="ID of an existing model or definition for a new one that is to be trained",
    )
    training: TrainingRun


class TrainingResult(TrainingBase):
    actual_training_time: Optional[int] = Field(
        None, ge=0, description="Actual time spend on training duration in seconds"
    )
    validation_error: Optional[float]
    training_error: float


class TrainingJob(Job):
    resource: TrainingBase
    result: Optional[TrainingResult]
