from typing import Optional, Dict, Any, Union
from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import Field
from app.core.base_model import BaseModel
from app.schemas.v2.data import InputData
from app.schemas.v2.job import Job



# Training
class TrainingBase(BaseModel):
    data: InputData
    max_training_time: Optional[int] = Field(..., gt=0, description="Maximum training duration in seconds")
    model_id: Optional[UUID] = Field(default_factory=UUID, description="ID of an existing model that is to be retrained")
    # Config as "just a dict" is not a good idea, depends on backend
    training_configuration: Optional[Dict[str,Any]]

class TrainingResult(TrainingBase):
    actual_training_time: Optional[int] = Field(..., gt=0, description="Actual time spend on training duration in seconds")
    validation_error: Optional[float]
    training_error: float
 
class TrainigJob(TrainingBase,Job):
    pass
