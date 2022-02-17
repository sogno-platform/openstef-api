from datetime import datetime
from typing import Optional
import uuid

from pydantic import Field

from app.core.base_model import BaseModel


# RESPONSE MODELS ######################################################################
class TrainModelTaskReponseModel(BaseModel):
    id: uuid.UUID = Field(
        ...,
        description="Id of the training task",
        example="02feacb5-1f5c-42fe-8577-4b96be473e0b"
    )
    training_done: bool = Field(
        ...,
        description="State of the training task, 'true' if done, 'false' otherwise",
        example=False
    )
    created: datetime = Field(
        ...,
        description="Datetime in UTC when the training task started",
        example="2021-05-12T18:00:28.248455+00:00"
    )
    duration: int = Field(
        ...,
        description="Duration of the model training task in seconds",
        example=65
    )
    trained_model_id: Optional[str] = Field()
    training_failed: Optional[bool] = Field(
        None,
        description="Indicates if the training task was succesful. None if not determined yet"
    )
    reason_failed: Optional[str] = Field(
        "", description="Reason why the training task failed"
    )
    new_model_better: Optional[bool] = Field(
        None,
        description="Whether or not the newly trained model was better. null if not finished"
    )
    trained_model_url: Optional[str] = Field(
        None,
        description="Url to dowload the trained model if finished, null if not finished",
        example="http://127.0.0.1:8000/api/v1/trained-models/02feacb5-1f5c-42fe-8577-4b96be473e0b"
    )
