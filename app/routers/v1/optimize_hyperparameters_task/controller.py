
from app.routers.v1.optimize_hyperparameters_task.api_models import OptimizeHyperparametersTaskResponseModel
from app.schemas.v1.db_models import OptimizeHyperparametersTask
from app.routers.v1.optimize_hyperparameters_task.repository import OptimizeHyperparametersTaskRepository


class OptimizeHyperparametersTaskController:
    """Hyperparameters controller.

        Provides the linking layer between the view (REST API interface) and the
        repository (storage).
    """

    def __init__(self) -> None:
        self.repository = OptimizeHyperparametersTaskRepository()

    def create_optimize_hyperparameters_task(
        self, id: str, prediction_job_id: int
    ) -> OptimizeHyperparametersTaskResponseModel:
        # NOTE: implicit conversion from db model to response model
        return self.repository.create_optimize_hyperparameters_task(
            id, prediction_job_id
        )

    def read_optimize_hyperparameters_task(
        self, id: str
    ) -> OptimizeHyperparametersTaskResponseModel:
        # NOTE: implicit conversion from db model to response model
        return self.repository.read_optimize_hyperparameters_task(id=id)

    def update_optimize_hyperparameters_task(
        self, task: OptimizeHyperparametersTask
    ) -> OptimizeHyperparametersTaskResponseModel:
        # NOTE: implicit conversion from db model to response model
        return self.repository.update_optimize_hyperparameters_task(task)
