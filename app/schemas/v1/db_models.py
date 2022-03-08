
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime

from app.common.database import Base


class TrainModelTask(Base):
    __tablename__ = "train_model_tasks"

    id = Column(String, primary_key=True, index=True)
    training_done = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer, default=0)
    trained_model_id = Column(String)
    training_failed = Column(Boolean)
    reason_failed = Column(String)
    new_model_better = Column(Boolean)


class OptimizeHyperparametersTask(Base):
    __tablename__ = "optimize_hyperparameters_tasks"

    id = Column(String, primary_key=True, index=True)
    optimize_done = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer, default=0)
    prediction_job_id = Column(Integer)
    optimize_failed = Column(Boolean)
    reason_failed = Column(String)
