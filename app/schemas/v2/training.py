from typing import Optional, Dict, Any, Union
from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import Field
from app.core.base_model import BaseModel
from app.schemas.v2.data import InputData
from app.schemas.v2.job import Job
from app.schemas.v2.model import PredModelBase



# Training
class TrainingBase(BaseModel):
    data: InputData
    max_training_time: Optional[int] = Field(..., ge=0, description="Maximum training duration in seconds")
    model: Union[int, PredModelBase] = Field(..., description="ID of an existing model or definition for a new one that is to be trained")
    # Config as "just a dict" is not a good idea, depends on backend
    training_configuration: Optional[Dict[str,Any]]

class TrainingResult(TrainingBase):
    actual_training_time: Optional[int] = Field(..., ge=0, description="Actual time spend on training duration in seconds")
    validation_error: Optional[float]
    training_error: float
 
class TrainingJob(Job):
    resource: TrainingBase
    result: Optional[TrainingResult]


