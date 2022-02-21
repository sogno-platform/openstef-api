from typing import Optional, Dict, Any, Union
from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import Field
from app.core.base_model import BaseModel
from app.schemas.v2.data import InputData
from app.schemas.v2.job import Job

# Prediction
class PredictionBase(BaseModel):
    data: InputData
    prediction_horizon: datetime
    model_id: UUID

class PredictionJob(PredictionBase,Job):
    pass