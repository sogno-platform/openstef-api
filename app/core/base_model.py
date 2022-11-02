"""Customize default BaseModel"""
from pydantic import BaseModel

BaseModel.Config.extra = "ignore"