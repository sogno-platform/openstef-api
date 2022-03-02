from venv import create
from fastapi import APIRouter
from typing import List, Optional
from uuid import UUID, uuid4
from app.schemas.v2.model import PredModel, PredModelBase
from app.database import redis_model
from .model_controller import *

router = APIRouter()


@router.get("/", response_model=List[int])  # , responses={})
async def all_models():
    """
    Get a list with all available model results.
    """
    ids = await get_all_model_ids()
    print(ids)
    return ids


@router.get("/{model_id}", response_model=PredModel)
async def get_model(model_id: UUID):
    return await get_model(model_id)


@router.post("/", response_model=PredModel)
async def create_model(data: PredModelBase):
    """
    Request a new model.
    """
    return await create_model(data)


@router.delete("/{model_id}", response_model=PredModel)
async def delete_model(model_id: UUID):
    """
    Delete a model.
    """
    return await delete_model(model_id)
