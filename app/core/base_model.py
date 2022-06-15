"""Customize default BaseModel"""
from proloaf.base import PydConfigurable as BaseModel

BaseModel.Config.extra = "ignore"