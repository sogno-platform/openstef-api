from app.routers.trained_model_task.v1.client import TrainModelTaskClient

import structlog

from app.models.v1.db_models import TrainModelTask
from app.utils import datetime_utc_now


class TrainModelTaskRepository:

    def __init__(self) -> None:
        self.logger = structlog.get_logger(self.__class__.__name__)
        self.client = TrainModelTaskClient()

    # Train model task CRUD ############################################################
    def create_train_model_task(self, train_task_id):
        train_model_task = TrainModelTask(id=train_task_id)
        return self.client.create_train_model_task(train_model_task)

    def read_train_model_task(self, train_task_id):
        train_model_task = self.client.read_train_model_task(train_task_id)

        if train_model_task is None:
            return

        # update training duration while we are training
        if train_model_task.training_done is False:
            train_model_task.duration = (datetime_utc_now() - train_model_task.created).seconds
            train_model_task = self.client.update_train_model_task(train_model_task)

        return train_model_task

    def update_train_model_task(self, train_model_task):
        return self.client.update_train_model_task(train_model_task)

    def delete_train_model_task(self, train_task_id):
        return self.client.delete_train_model_task(train_task_id)
