from fastapi import APIRouter
from typing import List, Optional
from uuid import UUID, uuid4
from app.schemas.v2.model import PredModel, PredModelBase


router = APIRouter()


@router.get("/", response_model=List[UUID])  # , responses={})
def all_models():
    """
    Get a list with all available model results.
    """
    pass


@router.get("/{model_id}", response_model=PredModel)
def get_model(model_id: UUID):
    pass


@router.post("/", response_model=PredModelBase)
def create_model(data: PredModelBase):
    """
    Request a new model.
    """
    pass


@router.delete("/{model_id}", response_model=PredModel)
def delete_model(model_id: UUID):
    """
    Delete a model.
    """
    pass
