from app.schemas.v1.db_models import OptimizeHyperparametersTask
from app.routers.v1.optimize_hyperparameters_task.client import OptimizeHyperparametersTaskClient


class OptimizeHyperparametersTaskRepository:

    def __init__(self) -> None:
        self.client = OptimizeHyperparametersTaskClient()

    def create_optimize_hyperparameters_task(
            self, id: str, prediction_job_id: int
    ) -> OptimizeHyperparametersTask:
        return self.client.create_optimize_hyperparameters_task(
            OptimizeHyperparametersTask(id=id, prediction_job_id=prediction_job_id)
        )

    def read_optimize_hyperparameters_task(
            self, id: str
    ) -> OptimizeHyperparametersTask:
        return self.client.read_optimize_hyperparameters_task(id)

    def update_optimize_hyperparameters_task(
        self, task: OptimizeHyperparametersTask
    ) -> OptimizeHyperparametersTask:
        return self.client.update_optimize_hyperparameters_task(task)
