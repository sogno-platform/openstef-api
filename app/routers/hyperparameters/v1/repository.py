import structlog


class HyperparametersRepository:

    def __init__(self) -> None:
        # TODO use adminstrative API
        self.client = None
        self.logger = structlog.get_logger(self.__class__.__name__)

    # Hyperparameters CRUD #############################################################
    def create_prediction_job_hyperparameters(self):
        # TODO
        return self.client.create_prediction_job_hyperparameters()

    def read_prediction_job_hyperparameters(self):
        # TODO
        return self.client.read_prediction_job_hyperparameters()

    def update_prediction_job_hyperparameters(self, id, hyperparameters):
        # TODO
        self.logger.info(f"Update hyperparameters for prediction job {id}: {hyperparameters}")
        return self.client.update_prediction_job_hyperparameters()

    def delete_prediction_job_hyperparameters(self):
        # TODO
        return self.client.delete_prediction_job_hyperparameters()
