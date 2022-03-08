from fastapi import APIRouter
from typing import List, Optional
from app.schemas.v2.training import TrainingBase, TrainingJob, TrainingResult
from . import training_controller as tc

router = APIRouter()


@router.get("/", response_model=List[int])  # , responses={})
async def all_trainings():
    """
    Get a list with all available Training results.
    """
    return await tc.get_all_training_ids()


@router.get("/{job_id}", response_model=TrainingJob)
async def get_training(
    job_id: int,
):
    return await tc.get_training(job_id)


@router.post("/", response_model=TrainingJob)
async def request_training(training_request: TrainingBase):
    """
    Request a new prediction.
    """
    return await tc.create_training_job(training_request)


@router.delete("/{job_id}", response_model=TrainingJob)
async def delete_training(job_id: int):
    """
    Request a new prediction.
    """
    return await tc.delete_training(job_id)
