"""Model definitions of API errors.

Contains a model of error responses.
"""

from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    detail: str  # error message
