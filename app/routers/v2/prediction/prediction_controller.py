import json
from app.common.database import redis_job, get_unique_id
from app.schemas.v2.prediction import PredictionBase, PredictionJob

from app.common.io import amqp_publisher

async def get_all_prediction_ids():
    keys = await redis_job.keys(pattern="pred_*")
    return [key.decode("utf-8").split("_")[-1] for key in keys]


async def get_prediction(id: int):
    job = await redis_job.get(f"pred_{id}")
    return PredictionJob(**json.loads(job))


async def create_prediction_job(data: PredictionBase):
    id = await get_unique_id()
    job = PredictionJob(resource=data, job_id=id)
    await redis_job.set(f"pred_{id}", job.json())
    await amqp_publisher.publish(f"prediction.{id}", job.dict())
    return job


# XXX Job not removed from queue (yet)
async def delete_prediction(id: int):
    job = await get_prediction(id)
    await redis_job.delete(f"pred_{id}")
    return job