import structlog

from app import database
from app.models.v1.db_models import OptimizeHyperparametersTask

optimize_hyperparameters_tasks_table = """
CREATE TABLE IF NOT EXIST `tst_icarus`.`optimize_hyperparameters_tasks` (
    `id` VARCHAR(36) NOT NULL ,
    `optimize_done` BOOLEAN NOT NULL ,
    `created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,
    `duration` INT(11) NOT NULL ,
    `prediction_job_id` INT(11) NOT NULL ,
    `optimize_failed` BOOLEAN NULL ,
    `reason_failed` VARCHAR(64) NULL ,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB;
ALTER TABLE `optimize_hyperparameters_tasks`
    ADD FOREIGN KEY (`prediction_job_id`)
    REFERENCES `predictions`(`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION;
"""


class OptimizeHyperparametersTaskClient:
    """Optimize hyperparameters task client

    """

    def __init__(self):
        self.logger = structlog.get_logger(self.__class__.__name__)

    def create_optimize_hyperparameters_task(
        self, task: OptimizeHyperparametersTask
    ) -> OptimizeHyperparametersTask:
        with database.get_session() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
        return task

    def read_optimize_hyperparameters_task(
        self, task_id: str
    ) -> OptimizeHyperparametersTask:
        with database.get_session() as session:
            query = session.query(OptimizeHyperparametersTask)
            query = query.filter(OptimizeHyperparametersTask.id == task_id)
            task = query.first()
        return task

    def update_optimize_hyperparameters_task(
        self, task: OptimizeHyperparametersTask
    ) -> OptimizeHyperparametersTask:
        with database.get_session() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
        return task

    def delete_optimize_hyperparameters_task(
        self, task_id: str
    ) -> OptimizeHyperparametersTask:
        with database.get_session() as session:
            query = session.query(OptimizeHyperparametersTask)
            query = query.filter(OptimizeHyperparametersTask.id == task_id)
            task = query.one_or_none()
            session.delete(task)
        return task
