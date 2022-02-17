"""Defines API endpoints. Uses `controller.py` to handle the actual logic"""


import zipfile
from io import SEEK_END, BytesIO
from typing import Optional

import structlog
from fastapi import (
    APIRouter,
    BackgroundTasks,
    HTTPException,
    Path,
    Query,
    Response,
    status,
    Body,
)
from openstef.model.serializer import MODEL_ID_SEP
from starlette.requests import Request
from starlette.responses import StreamingResponse

from app.core.settings import Settings
from app.models.v1 import utils
from app.routers.trained_model.v1.api_models import (
    TrainedModelTrainRequestModel,
    TrainedModelTrainResponseModel,
)
from app.routers.trained_model.v1.controller import TrainedModelController

router = APIRouter()

controller = TrainedModelController()

logger = structlog.get_logger(__name__)

background_task_counter = 0

uuid_path_parameter = Path(
    ...,
    description=f"Trained model id is using format {{pid}}{MODEL_ID_SEP}{{datetime}}",
    example="307-20210504150154",
    regex=f"^[0-9]{{3,4}}{MODEL_ID_SEP}[0-9]{{14}}$",
)


def train_model_task_runner(*args, **kwargs):
    """Run the train model task.

    Run the task and keep track of how many tasks are running.

    Args:
        args: Positional argument to the task function
        kwargs: Keyword arguments to the task function.
    """
    global background_task_counter
    background_task_counter += 1
    logger.info(
        f"Increment the train model task counter "
        f"from {background_task_counter - 1} to {background_task_counter}",
        background_task_counter=background_task_counter,
    )
    try:
        controller.train_model(*args, **kwargs)
    # Make sure we always decrement the background task counter even if an exception
    # occurs
    except Exception as e:
        logger.error(
            "Exception occured while running train model background task", exc_info=e
        )
    background_task_counter -= 1
    logger.info(
        f"Decrement the train model task counter "
        f"from {background_task_counter + 1} to {background_task_counter}",
        background_task_counter=background_task_counter,
    )


@router.post("/train", response_model=TrainedModelTrainResponseModel)
async def train_model(
    train_model_request: TrainedModelTrainRequestModel,
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
):
    """Train a model.
    For an input example, see data/*train_model_input*.json
    Returns:
        TrainedModelTrainResponseModel.
    """
    if background_task_counter >= Settings.max_background_tasks:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="To many train model tasks running",
        )

    task_id = utils.generate_uuid()

    background_tasks.add_task(
        train_model_task_runner,
        train_task_id=task_id,
        train_model_request=train_model_request,
    )

    status_url = str(request.url).replace(
        "/trained-models/train", f"/train-model-tasks/{task_id}"
    )

    response.headers["Location"] = status_url
    response.status_code = status.HTTP_202_ACCEPTED

    return TrainedModelTrainResponseModel(task_id=task_id, status_url=status_url)


@router.get("/{uuid}")
async def read_trained_model(uuid: str = uuid_path_parameter) -> StreamingResponse:
    """Get a trained model.

    Returns:
        StreamingResponse
    """
    try:
        model_path = controller.read_trained_model_path(uuid)
    except NameError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trained model not found"
        )

    return zip_models([model_path])


@router.delete("/{uuid}")
async def remove_trained_model(uuid: str = uuid_path_parameter):

    try:
        controller.remove_trained_model(uuid)
    except NameError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trained model not found"
        )


@router.get("/")
async def find_trained_models(
    prediction_job_id: int = Query(..., description="Prediction job id filter"),
    limit: Optional[int] = Query(1, description="Number of models to retrieve"),
    ascending: Optional[bool] = Query(
        False,
        description="Sorting order. Ascending is False will return the newest model(s) first.",
    ),
) -> StreamingResponse:
    """NOT IMPLEMENTED YET!
    Controller has nog function 'find_trained_model_paths yet

    Get trained models"""


    paths = controller.find_trained_model_paths(
        prediction_job_id=prediction_job_id, limit=limit, ascending=ascending
    )
    if len(paths) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No trained model found"
        )

    return zip_models(paths)


def zip_models(model_paths):
    filename = "trained_models.zip"
    relative_model_paths = []

    for model_path in model_paths:
        pid, model_datetime, model_file = model_path.parts[-3:]
        relative_path = f"{pid}/{model_datetime}/{model_file}"
        relative_model_paths.append(relative_path)

    # create buffer
    buffer = BytesIO()

    # zip models and write to buffer
    with zipfile.ZipFile(buffer, "w") as zf:
        for model_path, relative_path in zip(model_paths, relative_model_paths):
            zf.write(model_path, relative_path)

    # store number of bytes written
    buffer_length = buffer.seek(0, SEEK_END)
    # rewind buffer, IMPORTANT (response will be empty if not rewind)
    buffer.seek(0)

    response = StreamingResponse(buffer, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Length"] = str(buffer_length)

    return response
