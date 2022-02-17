"""Defines request and response data models"""
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field, validator

from app.core.base_model import BaseModel


class ForecastType(Enum):
    DEMAND = "demand"
    BASECASE = "basecase"
    DEFAULT = "default"
    SOLAR = "solar"
    WIND = "wind"


FORECAST_TYPES_STR = ", ".join([f'"{t.value}"' for t in ForecastType])


class FeatureType(Enum):
    MARKET_DATA = "market_data"
    WEATHER_DATA = "weather_data"
    LOAD_PROFILES = "load_profiles"


class FeatureModel(BaseModel):
    # required fields
    name: str = Field(..., description="Name of the feature", example="windspeed")
    data: List[Union[float, int, bool, str, None]] = Field(
        ...,
        description="Value of the feature at the given date time index",
        example=[2.89352, 2.71230, 2.56142],
    )
    # optional fields
    unit: Optional[str] = Field(description="Unit of the feature", example="m/s")
    type: Optional[FeatureType] = Field(
        description="Type of the feature", example=FeatureType.WEATHER_DATA
    )


class QuantileModel(BaseModel):
    quantile: float = Field(..., description="", example=0.95)
    value: List[float] = Field(..., description="")


class InputdataModel(BaseModel):
    """Input data model.

    The input data request model is base on pandas.DataFrame.to_json() when using
    orient="split". This makes it really convenient to convert to and from a pandas
    DataFrame.
    """

    index: List[datetime] = Field(
        ...,
        description="Datetime index of load and features",
        # TODO better example
        example=[
            "2021-04-30T14:00:00.000Z",
            "2021-04-30T14:15:00.000Z",
            "2021-04-30T14:30:00.000Z",
        ],
    )
    columns: List[str] = Field(
        ...,
        description="The names of the columns",
        example=["load", "feature_one", "feature_two"],
    )
    data: List[List[Union[float, int, str, None]]] = Field(
        ...,
        description="The data of the columns",
        # TODO better example
        example=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    )

    @validator("columns")
    def columns_should_contain_load(cls, v):
        if "load" not in v:
            raise ValueError("'load' is a required column")
        return v


# TODO: right now the PredictionJobModel has a lot of defaults, eventhough specific
# endpoints require different attributes to be defined. This means right now the
# validation is not really that strict. We need to improve this.
#
# required prediction job properties based on the core pipeline
# train model:
#   "name", "model", "hyper_params", "feature_names"
# generate forecast:
#   "name", "id", "resolution_minutes", "horizon_minutes", "type", "model_type_group",
#   "quantiles"
# optimize hyperparams:
#   "name", "model"


class PredictionJobModel(BaseModel):
    """Prediction job model."""

    id: Union[int, str] = Field(
        ...,
        description="Load the most recent model tagged with this prediction job id",
        example=307,
    )
    name: str = Field(..., description="Name")
    description: str = Field("", description="Description")
    forecast_type: ForecastType = Field(
        ForecastType.DEMAND, description="The forecast type."
    )
    model_type: str = Field("xgb", description="The model type.")
    model_type_group: str = Field("")
    horizon_minutes: int = Field(
        2880, description="Prediction horizon in minutes", example=2880
    )
    resolution_minutes: int = Field(
        15, description="Resolution of the prediction in minutes", example=15
    )
    quantiles: List[float] = Field(
        [0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95],
        description="Quantiles to predict",
        example=[0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95],
    )
    hyperparameters: dict = Field(
        default_factory=dict,
        description="The model specific hyperparameters",
        example={
            "subsample": 0.5252878607665824,
            "min_child_weight": 6,
            "max_depth": 6,
            "gamma": 0.6632692035430702,
            "colsample_bytree": 0.8916557311879749,
            "silent": 1,
            "objective": "reg:squarederror",
            "eta": 0.0749324689383426,
            "featureset_name": "C",
            "training_period_days": 90,
        },
    )
    feature_names: List[str] = Field(
        ["windspeed", "radiation", "is_saturday", "T-7d"],
        description="The features (previously) used to train the model",
        example=["windspeed", "radiation", "is_saturday", "T-7d"],
    )
