"""Defines request and response data models"""
from app.models.v1.shared_models import InputdataModel, PredictionJobModel
from pydantic import Field

from app.core.base_model import BaseModel


# REQUEST MODELS #######################################################################
class TrainedModelTrainRequestModel(BaseModel):
    """Trained model request model.
    """
    input_data: InputdataModel
    prediction_job: PredictionJobModel
    maximum_model_age: int = Field(
        None,
        description=(
            "The maximum (old) model age in days. A new model will only be trained if "
            "the old model is older then `maximum_model_age`. "
        )
    )
    compare_to_old_model: bool = Field(
        False,
        description=(
            "Compare the newly trained model to the latest previously trained model "
            "(if any). If the new model is worse, don't store the new model."
        )
    )


# RESPONSE MODELS ######################################################################
class TrainedModelTrainResponseModel(BaseModel):
    """Trained model response model.
    """
    task_id: str = Field(..., description="Train model task id")
    status_url: str = Field(..., description="Train model status url")
