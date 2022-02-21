import structlog
#from openstef.pipeline.optimize_hyperparameters import optimize_hyperparameters_pipeline

from app.routers.v1.hyperparameters.repository import HyperparametersRepository
from app.routers.v1.hyperparameters.api_models import (
    OptimizeHyperparametersRequestModel,
)
from app.routers.v1.optimize_hyperparameters_task.controller import (
    OptimizeHyperparametersTaskController,
)
from app.schemas.v1.utils import (
    input_data_model_to_input_data_df,
    prediction_job_request_model_to_prediction_job_dict,
)
from app.utils import datetime_utc_now


class HyperparametersController:
    """Hyperparameters controller.

    Provides the linking layer between the view (REST API interface) and the
    repository (storage).
    """

    def __init__(self) -> None:
        self.task_controller = OptimizeHyperparametersTaskController()
        self.repository = HyperparametersRepository()
        self.logger = structlog.get_logger(self.__class__.__name__)

    def optimize_hyperparameters(
        self, task_id: str, request_model: OptimizeHyperparametersRequestModel
    ):
        # convert request model to internal model (dict and dataframe)
        input_data = input_data_model_to_input_data_df(request_model.input_data)
        prediction_job = prediction_job_request_model_to_prediction_job_dict(
            request_model.prediction_job
        )

        # create optimize hyperparameters task
        task = self.task_controller.create_optimize_hyperparameters_task(
            id=task_id, prediction_job_id=request_model.prediction_job.id
        )
        self.logger.info("Created optimize hyperparamters task", task_id=task.id)

        # optimize hyperparameters
        try:
            self.logger.info("Start optimizing hyperparameters")
            input_data = input_data.sort_index()
            hyperparameters = optimize_hyperparameters_pipeline(
                prediction_job, input_data
            )
        # this happens when the input data is insufficient
        except ValueError as e:
            msg = "Input data was insufficient"
            task.optimize_failed = True
            task.reason_failed = msg
            self.logger.error(msg, exc_info=e)
        # catch all for unknown exceptions
        except Exception as e:
            msg = f"Unknown exception occured: {e}"
            task.optimize_failed = True
            task.reason_failed = msg
            self.logger.error(msg, exc_info=e)
        # optimizing did not raise an exception -> hyperparameters where optimized
        else:
            task.optimize_failed = False
            task.reason_failed = ""

            # update current hyperparameters
            self.repository.update_prediction_job_hyperparameters(
                id=request_model.prediction_job.id, hyperparameters=hyperparameters
            )

            # set generic task properties
            task.optimize_done = True
            # TODO
            task.hyperparameters_url = "Not implemented"
            task.duration = (datetime_utc_now() - task.created).seconds
            self.logger.info(
                "Finished optimizing hyperparameters successfully",
                duration=task.duration,
            )

        # always update the task
        self.task_controller.update_optimize_hyperparameters_task(task)
