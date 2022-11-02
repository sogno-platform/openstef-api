from __future__ import annotations
from typing import Optional
from enum import Enum
from datetime import datetime
from .data import InputDataFormat
from .job import Job
from .proloaf_api_models import ModelWrapper as Model
from app.core.base_model import BaseModel
from pydantic import Field


class ModelType(str, Enum):
    # TODO Placeholder
    model1 = "model1"
    model2 = "model2"


class PredModelBase(BaseModel):
    name: Optional[str]
    model_type: ModelType
    model: Optional[Model]


class PredModel(PredModelBase):
    model_id: int
    date_trained: Optional[datetime]
    date_hyperparameter_tuned: Optional[datetime]
    predicted_feature: Optional[str]
    expected_data_format: Optional[InputDataFormat]


class PredModelCreationJob(Job):
    resource: PredModelBase
    result: Optional[PredModel]