"""Defines API endpoints. Uses `controller.py` to handle the actual logic"""

import uuid

from app.routers.v1.optimize_hyperparameters_task.api_models import (
    OptimizeHyperparametersTaskResponseModel
)
from fastapi import APIRouter, status, Request
from fastapi.exceptions import HTTPException
import structlog

from app.routers.v1.optimize_hyperparameters_task.controller import (
    OptimizeHyperparametersTaskController
)

router = APIRouter()

controller = OptimizeHyperparametersTaskController()

logger = structlog.get_logger(__name__)


@router.get(
    "/{uuid}",
    response_model=OptimizeHyperparametersTaskResponseModel,
    status_code=status.HTTP_202_ACCEPTED
)
async def get_optimize_hyperparameters_task(
    uuid: uuid.UUID,
    request: Request
) -> OptimizeHyperparametersTaskResponseModel:
    """Get the status of the hyperparameters being optimized.

    Response:
        OptimizeHyperparametersTaskResponseModel
    """
    task = controller.read_optimize_hyperparameters_task(str(uuid))

    # no status found
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Optimize hyperparameters status not found"
        )

    return task
