from app.database import redis_model, get_unique_id
from app.schemas.v2.model import PredModelBase, PredModel

async def get_all_model_ids():
    return await redis_model.keys()

async def get_model(id:int):
    return await redis_model.get(id)

async def create_model(data:PredModelBase):
    id = await get_unique_id()
    model = PredModel(**data.dict(), model_id = id)
    await redis_model.set(id,model)
    return model

async def delete_model(id:int):
    model_dict = await redis_model.get(id)
    model = PredModel(**model_dict)
    await redis_model.delete(id)
    return model