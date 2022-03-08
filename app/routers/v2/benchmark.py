from fastapi import APIRouter
from typing import List, Optional
from uuid import UUID, uuid4
from app.schemas.v2.data import InputData
# from app.schemas.v2.benchmark import Benchmark

raise NotImplementedError("This endpoint has not been implemented")

router = APIRouter(prefix="/benchmark", tags=["benchmark"])


@router.get("/", response_model=List[UUID])  # , responses={})
def all_bechmarks():
    """
    Get a list with all available prediction results.
    """
    pass


# @router.get("/{benchmark_id}", response_model=InputData)
# def get_benchmark(benchmark_id: UUID):
#     pass


# @router.post("/", response_model=UUID)  # , responses={})
# def request_benchmark(data: Benchmark):
#     """
#     Request a new prediction.
#     """
#     pass


# @router.delete("/{benchmark_id}", response_model=Data)
# def delete_benchmark(benchmark_id: UUID):
#     """
#     Delete a prediction.
#     """
#     pass
