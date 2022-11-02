from fastapi import APIRouter
from typing import List, Optional

# import structlog
from app.schemas.v2.model import (
    PredModel,
    PredModelBase,
    PredModelCreationJob,
    ModelType,
)
from . import model_controller as mc

router = APIRouter()


@router.get("/", response_model=List[int])  # , responses={})
async def all_models():
    """
    Get a list with all available model results.
    """
    return await mc.get_all_model_ids()



@router.get("/{model_id}", response_model=PredModel)
async def get_model(model_id: int):
    return await mc.get_model(model_id)


@router.post("/", response_model=PredModelCreationJob)
async def create_model(data: PredModelBase):
    """
    Request a new model.
    """
    return await mc.create_model(data)


@router.delete("/{model_id}", response_model=PredModel)
async def delete_model(model_id: int):
    """
    Delete a model.
    """
    return await mc.delete_model(model_id)
