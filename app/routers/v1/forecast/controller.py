"""Classes that implement business logic / use cases regarding forecasts.

Classes:
    ForecastController: implements forecast functionality
"""

import pandas as pd
# from openstef.pipeline.create_basecase_forecast import create_basecase_forecast_pipeline
# from openstef.pipeline.create_forecast import create_forecast_pipeline_core

from app.common.exceptions import ModelNotFoundError
from app.schemas.v1.utils import (
    forecast_df_to_forecast_model,
    prediction_job_request_model_to_prediction_job_dict,
)
from app.routers.v1.forecast.api_models import (
    ForecastRequestModel,
    ForecastResponseModel,
)
from pathlib import Path
# from openstef.model.serializer import MLflowSerializer


class ForecastController:
    """Forecast controller.

    Provides the linking layer between the view (REST API interface) and the
    repository (storage).
    """

    def generate_forecast(
        self, forecast_request: ForecastRequestModel
    ) -> ForecastResponseModel:
        """Generate a forecast

        Returns:
            ForecastResponseModel
        """
        # convert request model to internal model (dict and dataframe)
        input_data = pd.DataFrame(**forecast_request.input_data.dict())
        prediction_job = prediction_job_request_model_to_prediction_job_dict(
            forecast_request.prediction_job
        )
        pid = forecast_request.prediction_job.id
        serializer = MLflowSerializer(
            trained_models_folder=Path("/data/icarus/visuals/trained_models")
        )
        model, model_specs = serializer.load_model(pid)

        # call pipeline to make a forecast
        forecast = create_forecast_pipeline_core(prediction_job, input_data, model)

        return forecast_df_to_forecast_model(forecast)

    def generate_basecase_forecast(
        self, forecast_request: ForecastRequestModel
    ) -> ForecastResponseModel:
        # convert request model to internal model (dict and dataframe)
        input_data = pd.DataFrame(**forecast_request.input_data.dict())
        prediction_job = prediction_job_request_model_to_prediction_job_dict(
            forecast_request.prediction_job
        )
        forecast = create_basecase_forecast_pipeline(prediction_job, input_data)

        return forecast_df_to_forecast_model(forecast)
