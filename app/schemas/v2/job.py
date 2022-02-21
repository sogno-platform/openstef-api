from typing import Optional, Dict, Any, Union
from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import Field
from app.core.base_model import BaseModel
from app.schemas.v2.data import InputData


class JobStatus(str, Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

class Job(BaseModel):
    job_id: UUID
    status: JobStatus
