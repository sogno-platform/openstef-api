from fastapi import APIRouter
from typing import List, Optional
from uuid import UUID, uuid4
from app.schemas.v2.data import InputData, TimeseriesData
from app.schemas.v2.prediction import PredictionBase, PredictionJob
from . import prediction_controller as pc


router = APIRouter()


@router.get("/", response_model=List[int])  # , responses={})
async def all_prediction():
    """
    Get a list with all available prediction results.
    """
    return await pc.get_all_prediction_ids()


@router.get("/{job_id}", response_model=PredictionJob)
async def get_prediction(job_id: int):
    return await pc.get_prediction(job_id)


@router.post("/", response_model=PredictionJob)  # , responses={})
async def request_prediction(data: PredictionBase):
    """
    Request a new prediction.
    """
    return await pc.create_prediction_job(data)


@router.delete("/{job_id}", response_model=PredictionJob)
async def delete_prediction(job_id: int):
    """
    Delete a prediction.
    """
    return await pc.delete_prediction(job_id)
