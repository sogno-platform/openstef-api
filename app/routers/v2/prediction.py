from fastapi import APIRouter
from typing import List, Optional
from uuid import UUID, uuid4
from app.schemas.v2.data import InputData, TimeseriesData
from app.schemas.v2.prediction import PredictionBase


router = APIRouter()


@router.get("/", response_model=List[UUID])  # , responses={})
def all_prediction():
    """
    Get a list with all available prediction results.
    """
    pass


@router.get("/{prediction_id}", response_model=TimeseriesData)
def get_prediction(prediction_id: UUID):
    pass


@router.post("/", response_model=UUID)  # , responses={})
def request_prediction(data: PredictionBase):
    """
    Request a new prediction.
    """
    pass


@router.delete("/{prediction_id}", response_model=TimeseriesData)
def delete_prediction(prediction_id: UUID):
    """
    Delete a prediction.
    """
    pass
