from typing import Optional, Dict, Any, Union
from enum import Enum
from uuid import UUID
from datetime import datetime
from app.core.base_model import BaseModel
from app.schemas.v2.data import InputDataFormat


class ModelType(str,Enum):
    #TODO Placeholder
    model1 = "model1"
    model2 = "model2"

class PredModelBase(BaseModel):
    name: Optional[str]
    model_type: ModelType
    # XXX "just a dict" is not a comprehensible typdefinition 
    model_definition: Optional[Dict[str,Any]]

class PredModel(PredModelBase):
    model_id: UUID
    date_trained: Optional[datetime]
    date_hyperparameter_tuned: Optional[datetime]
    predicted_feature: Optional[str]
    # XXX see if DataDefinition is a necessary/reasonable thing to have
    expected_data_format: Optional[InputDataFormat]