import structlog

from app import database
from app.schemas.v1.db_models import TrainModelTask

# TODO (FRANK): the tasks_table appears to not be used (anymore?)
tasks_table = """
    CREATE TABLE IF NOT EXIST `tst_icarus`.`tasks` (
        `id` VARCHAR(36) NOT NULL ,
        `training_done` BOOLEAN NOT NULL ,
        `created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,
        `duration` INT NOT NULL ,
        `trained_model_id` INT NOT NULL ,
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB;
"""


class TrainModelTaskClient:
    """Trained model task client

    """

    def __init__(self):
        self.logger = structlog.get_logger(self.__class__.__name__)

    def create_train_model_task(self, task: TrainModelTask) -> TrainModelTask:
        with database.get_session() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
        return task

    def read_train_model_task(self, task_id: str) -> TrainModelTask:
        with database.get_session() as session:
            query = session.query(TrainModelTask)
            query = query.filter(TrainModelTask.id == task_id)
            task = query.first()
        return task

    def update_train_model_task(self, task: TrainModelTask) -> TrainModelTask:
        with database.get_session() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
        return task

    def delete_train_model_task(self, task_id: str) -> TrainModelTask:
        with database.get_session() as session:
            query = session.query(TrainModelTask)
            query = query.filter(TrainModelTask.id == task_id)
            task = query.one_or_none()
            session.delete(task)
        return task
