from fastapi import APIRouter
from typing import List, Optional
from uuid import UUID, uuid4
from app.schemas.v2.training import TrainingBase, TrainingResult


router = APIRouter()


@router.get("/", response_model=List[TrainingResult])  # , responses={})
def all_trainings():
    """
    Get a list with all available Training results.
    """
    pass


@router.get("/{training_id}", response_model=TrainingResult)
def get_training(
    training_id: UUID,
):
    pass


@router.post("/", response_model=UUID)
def request_training(training_request: TrainingBase):
    """
    Request a new prediction.
    """
    pass


@router.delete("/{training_id}", response_model=TrainingResult)
def delete_training(training_id: UUID):
    """
    Request a new prediction.
    """
    pass
