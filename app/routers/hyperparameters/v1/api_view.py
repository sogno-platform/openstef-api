"""Defines API endpoints. Uses `controller.py` to handle the actual logic"""
from fastapi import APIRouter, BackgroundTasks, Request, Response, status
from fastapi.exceptions import HTTPException
import structlog

from app.core.settings import Settings
from app.models.v1 import utils
from app.routers.hyperparameters.v1.api_models import (
    OptimizeHyperparametersRequestModel, OptimizeHyperparametersResponseModel
)
from app.routers.hyperparameters.v1.controller import HyperparametersController

router = APIRouter()

controller = HyperparametersController()

logger = structlog.get_logger(__name__)

background_task_counter = 0


def optimize_hyperparameters_task_runner(*args, **kwargs):
    """Run the optimize hyperparameters task.

    Run the task and keep track of how many tasks are running.

    Args:
        args: Positional argument to the task function
        kwargs: Keyword arguments to the task function.
    """
    global background_task_counter
    background_task_counter += 1
    logger.info(
        f"Increment the optimize hyperparameters task counter "
        f"from {background_task_counter - 1} to {background_task_counter}",
        background_task_counter=background_task_counter
    )
    try:
        controller.optimize_hyperparameters(*args, **kwargs)
    # Make sure we always decrement the background task counter even if an exception
    # occurs
    except Exception as e:
        logger.error(
            "Exception occured while running optimize hyperparameters background task",
            exc_info=e
        )
    background_task_counter -= 1
    logger.info(
        f"Decrement the optimize hyperparameters task counter "
        f"from {background_task_counter + 1} to {background_task_counter}",
        background_task_counter=background_task_counter
    )


@router.post("/optimize", response_model=OptimizeHyperparametersResponseModel)
async def optimize_hyperparameters(
    optimize_hyperparameters_request: OptimizeHyperparametersRequestModel,
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks
):
    """Optimize hyperparameters.

    Returns:
        dict: Optimized hyperparameters
    """

    if (background_task_counter >= Settings.max_background_tasks):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="To many optimize hyperparameters tasks running"
        )

    task_id = utils.generate_uuid()

    background_tasks.add_task(
        optimize_hyperparameters_task_runner,
        task_id=task_id,
        optimize_hyperparameters_request=optimize_hyperparameters_request
    )

    status_url = str(
        request.url
    ).replace(
        "/hyperparameters/optimize",
        f"/optimize-hyperparameters-tasks/{task_id}"
    )

    response.headers["Location"] = status_url
    response.status_code = status.HTTP_202_ACCEPTED

    return OptimizeHyperparametersResponseModel(task_id=task_id, status_url=status_url)
