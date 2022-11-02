import json
import logging
import structlog
from fastapi import BackgroundTasks
from app.common.database import redis_model, redis_job, get_unique_id
from app.schemas.v2.model import PredModelBase, PredModel, PredModelCreationJob
from app.common.io import amqp_publisher

logger = structlog.get_logger(__name__)
async def get_all_model_ids():
    keys = await redis_model.keys(pattern = "model_*")
    return [key.decode("utf-8").split("_")[-1] for key in keys]

async def get_model(id:int):
    json_model = None
    json_model = json.loads(await redis_model.get(f"model_{id}"))
    if json_model is None:
        # logger.info(f"Model with ID {id} was requested but does not exist in Database.")
        model = None
    else:
        model = PredModel(**json_model)
    
    return model


async def create_model(data:PredModelBase):
    id = await get_unique_id()
    # model = PredModel(**data.dict(), model_id = mode_id)
    job = PredModelCreationJob(job_id=id,resource=data)
    res = await redis_job.set(f"model_{id}",job.json())
    await amqp_publisher.publish(f"model.{id}", job.dict())
    return job

async def delete_model(id:int):
    model = await get_model(id)
    await redis_model.delete(f"model_{id}")
    return model