import uuid
from builtins import getattr

import pandas as pd

from app.schemas.v1.shared_models import (
    InputdataModel,
    PredictionJobModel,
    QuantileModel,
)
from app.routers.v1.forecast.api_models import (
    ForecastRequestModel,
    ForecastResponseModel,
)


def input_data_model_to_input_data_df(input_data: InputdataModel):
    return pd.DataFrame(**input_data.dict())


prediction_job_key_map = {
    # dict key: model attr
    "id": "id",
    "name": "name",
    "model": "model_type",
    "model_type_group": "model_type_group",
    "forecast_type": "forecast_type",
    "horizon_minutes": "horizon_minutes",
    "resolution_minutes": "resolution_minutes",
    "quantiles": "quantiles",
    "hyper_params": "hyperparameters",
    "feature_names": "feature_names",
    "description": "description",
}


def prediction_job_request_model_to_prediction_job_dict(
    prediction_job: PredictionJobModel,
) -> dict:
    prediction_job_dict = {}
    for d_key, m_attr in prediction_job_key_map.items():
        prediction_job_dict[d_key] = getattr(prediction_job, m_attr)

    return prediction_job_dict


def prediction_job_dict_to_prediction_job_model(
    prediction_job: dict,
) -> PredictionJobModel:
    kwargs = {
        m_attr: prediction_job[d_key]
        for d_key, m_attr in prediction_job_key_map.items()
    }
    return PredictionJobModel(**kwargs)


def forecast_df_to_forecast_model(forecast: pd.DataFrame) -> ForecastResponseModel:
    # convert forecast -> forecast response model
    quantiles = []

    for quantile_column in filter(
        lambda c: c.startswith("quantile_P"), forecast.columns
    ):
        quantile = QuantileModel(
            quantile=float(quantile_column.split("quantile_P")[1]) / 100.0,
            value=list(forecast[quantile_column]),
        )
        quantiles.append(quantile)

    forecast_response = ForecastResponseModel(
        index=list(forecast.index),
        forecast=list(forecast.forecast),
        stdev=list(forecast.stdev),
        quantiles=quantiles,
    )
    return forecast_response


def forecast_model_to_forecast_df(forecast: ForecastResponseModel) -> pd.DataFrame:
    index = pd.to_datetime(forecast.index, utc=True)
    data = {
        "forecast": forecast.forecast,
        "stdev": forecast.stdev,
    }
    for quantile in forecast.quantiles:
        column_name = f"quantile_P{quantile.quantile * 100:02.0f}"
        data[column_name] = quantile.value

    return pd.DataFrame(index=index, data=data)


def forecast_model_dict_to_forecast_df(forecast: ForecastResponseModel) -> pd.DataFrame:
    index = pd.to_datetime(forecast["index"], utc=True)
    data = {
        "forecast": forecast["forecast"],
        "stdev": forecast["stdev"],
    }
    for quantile in forecast["quantiles"]:
        column_name = f'quantile_P{quantile["quantile"] * 100:02.0f}'
        data[column_name] = quantile["value"]

    return pd.DataFrame(index=index, data=data)


def generate_uuid():
    return str(uuid.uuid4())
