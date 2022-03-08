from typing import Optional, Dict, Any, Union
from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import Field
from app.core.base_model import BaseModel
from app.schemas.v2.data import InputData,TimeseriesData
from app.schemas.v2.job import Job

# Prediction
class PredictionBase(BaseModel):
    input_data: InputData
    prediction_horizon: datetime
    model_id: int

class PredicitonResult(PredictionBase):
    output_data: TimeseriesData

class PredictionJob(Job):
    resource: PredictionBase
    result: Optional[PredicitonResult]