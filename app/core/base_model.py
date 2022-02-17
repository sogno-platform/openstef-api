"""Customize default BaseModel"""
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    """Base model for API request and response models.
    """
    # Introduced after the upgrade of FastAPI to 0.30.0, which required the use of
    # the orm_mode attribute, to maintain its behavior:
    # https://fastapi.tiangolo.com/release-notes/#0300

    # With `orm_mode == True`, an arbitrary class can be implicitely parsed
    # into a Pydantic model if the attribute names match. This simplifies
    # the conversion from your app's internal (business) data models to and from
    # the API data models as no custom conversion code has to be written.

    class Config:
        orm_mode = True
