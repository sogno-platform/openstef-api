import uuid

from fastapi import APIRouter, HTTPException, status, Body
from starlette.requests import Request

from app.routers.trained_model_task.v1.api_models import TrainModelTaskReponseModel
from app.routers.trained_model_task.v1.controller import TrainModelTaskController

router = APIRouter()

controller = TrainModelTaskController()

@router.get(
    "/{uuid}",
    response_model=TrainModelTaskReponseModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def get_train_model_task(
    uuid: uuid.UUID, request: Request
) -> TrainModelTaskReponseModel:
    """Get the status of a model being trained.

    Response:
        TrainingStatusResponseModel
    """
    task = controller.read_train_model_task(str(uuid))

    # no status found
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Train model status not found"
        )
    if task.training_done and task.new_model_better:
        trained_model_url = str(request.url).replace(
            f"/train-model-tasks/{uuid}", f"/trained-models/{task.trained_model_id}"
        )
    else:
        trained_model_url = None

    task.trained_model_url = trained_model_url

    return task
