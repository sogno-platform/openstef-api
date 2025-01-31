from typing import Optional, Dict, Any, Union
from enum import Enum
from uuid import UUID
from datetime import date, datetime
from pydantic import Field, validator
from app.core.base_model import BaseModel
from .data import InputData


class JobStatus(str, Enum):
    pending = "pending"
    doing = "doing"
    success = "success"
    failed = "failed"


class Job(BaseModel):
    job_id: int
    status: JobStatus = JobStatus.pending
    created: datetime = Field(default_factory=datetime.utcnow)
    result: Optional[Any]
    resource: Optional[Any]
    # value will just be status instead of (status,None) if no result
    # @validator("status","result")
    # def test_val(cls,value):
    #     print(value)
    #     status,result = value
    #     if status == JobStatus.success :
    #         assert result is not None, "If the job was successful it should have a result"
    #     return value
