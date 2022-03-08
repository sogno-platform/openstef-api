import json

from app.common.database import redis_job, get_unique_id
from app.common.io import amqp_publisher
from app.schemas.v2.training import *

async def get_all_training_ids():
    keys = await redis_job.keys(pattern="train_*")
    return [key.decode("utf-8").split("_")[-1] for key in keys]


async def get_training(id: int):
    job = await redis_job.get(f"train_{id}")
    # XXX serialization not strictly necessary if everything is valid
    return TrainingJob(**json.loads(job))


async def create_training_job(data: TrainingBase):
    id = await get_unique_id()
    job = TrainingJob(resource=data, job_id=id)
    await redis_job.set(f"train_{id}", job.json())
    await amqp_publisher.publish(f"training.{id}", job.dict())
    return job


# XXX Job not removed from queue (yet)
async def delete_training(id: int):
    job = await get_training(id)
    await redis_job.delete(f"train_{id}")
    return job