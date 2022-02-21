import pandas as pd
import structlog
from pathlib import Path
# from openstef.exceptions import (
#     InputDataInsufficientError,
#     InputDataWrongColumnOrderError,
#     OldModelHigherScoreError,
# )
# from openstef.pipeline.train_model import train_model_pipeline_core

from app.schemas.v1.shared_models import FeatureModel
from app.schemas.v1.utils import (
    input_data_model_to_input_data_df,
    prediction_job_request_model_to_prediction_job_dict,
)
# from openstef.data_classes.model_specifications import ModelSpecificationDataClass
from app.routers.v1.trained_model.api_models import TrainedModelTrainRequestModel

# from openstef.model.serializer import MLflowSerializer
from app.routers.v1.trained_model_task.controller import TrainModelTaskController
from app.utils import datetime_utc_now


class TrainedModelController:
    """Forecast controller.

    Provides the linking layer between the view (REST API) and repository (storage).
    """

    def __init__(self):
        self.task_controller = TrainModelTaskController()
        self.logger = structlog.get_logger(self.__class__.__name__)

    def train_model(
        self, train_task_id, train_model_request: TrainedModelTrainRequestModel
    ):
        """Train a model

        Returns:
            None
        """
        # convert request model to internal model (dict and dataframe)
        input_data = input_data_model_to_input_data_df(train_model_request.input_data)
        prediction_job = prediction_job_request_model_to_prediction_job_dict(
            train_model_request.prediction_job
        )

        # create train model task
        train_model_task = self.task_controller.create_train_model_task(train_task_id)
        self.logger.info(
            "Created train model task", train_model_task_id=train_model_task.id
        )
        self.logger.info(f"Finding model for pid {prediction_job['id']}")

        # train a model
        model_specs = ModelSpecificationDataClass(
            **{
                "id": prediction_job["id"],
                "hyper_params": {
                    "subsample": 0.9650102355823993,
                    "min_child_weight": 3,
                    "max_depth": 6,
                    "gamma": 0.1313691782115394,
                    "colsample_bytree": 0.8206844265155975,
                    "silent": 1,
                    "objective": "reg:squarederror",
                    "eta": 0.010025843216782565,
                    "training_period_days": 90,
                },
                "feature_names": [
                    "clearSky_dlf",
                    "clearSky_ulf",
                    "clouds",
                    "humidity",
                    "mxlD",
                    "pressure",
                    "radiation",
                    "rain",
                    "snowDepth",
                    "temp",
                    "winddeg",
                    "windspeed",
                    "windspeed_100m",
                    "sjv_E1A",
                    "sjv_E1B",
                    "sjv_E1C",
                    "sjv_E2A",
                    "sjv_E2B",
                    "sjv_E3A",
                    "sjv_E3B",
                    "sjv_E3C",
                    "sjv_E3D",
                    "T-15min",
                    "T-30min",
                    "T-45min",
                    "T-1200min",
                    "T-2160min",
                    "T-2d",
                    "T-3d",
                    "T-4d",
                    "T-5d",
                    "T-6d",
                    "T-7d",
                    "T-8d",
                    "T-9d",
                    "T-10d",
                    "T-11d",
                    "T-12d",
                    "T-13d",
                    "T-14d",
                    "IsWeekendDay",
                    "IsWeekDay",
                    "windpowerFit_harm_arome",
                    "saturation_pressure",
                    "vapour_pressure",
                    "air_density",
                    "dtemp_day",
                    "dtemp_week",
                    "dwindspeed_week",
                    "dwindspeed_100m_day",
                    "dwindspeed_100m_week",
                    "dwinddeg_day",
                    "dwinddeg_week",
                    "dpressure_hour",
                    "dpressure_week",
                    "dhumidity_hour",
                    "dhumidity_day",
                    "dhumidity_week",
                    "dair_density_hour",
                    "dair_density_day",
                    "dair_density_week",
                ],
            }
        )
        try:
            self.logger.info("Start training model")
            model, report, trained_model_specs = train_model_pipeline_core(
                prediction_job, model_specs, input_data
            )
        except InputDataInsufficientError as e:
            msg = "Input data was insufficient"
            train_model_task.training_failed = True
            train_model_task.reason_failed = msg
            train_model_task.new_model_better = False
            self.logger.error(msg, exc_info=e)
        except InputDataWrongColumnOrderError as e:
            msg = "Input data has wrong column order"
            train_model_task.training_failed = True
            train_model_task.reason_failed = msg
            train_model_task.new_model_better = False
            self.logger.error(msg, exc_info=e)
        except OldModelHigherScoreError as e:
            msg = "Old model was better then new model"
            train_model_task.training_failed = False
            train_model_task.reason_failed = msg
            train_model_task.new_model_better = False
            self.logger.error(msg, exc_info=e)
        # Catch all for unknown exceptions
        except Exception as e:
            msg = f"Unknown exception occured: {e}"
            train_model_task.training_failed = True
            train_model_task.reason_failed = msg
            train_model_task.new_model_better = False
            self.logger.error(msg, exc_info=e)
        # training did not raise an exception -> the new model was better
        else:
            train_model_task.training_failed = False
            train_model_task.reason_failed = ""
            train_model_task.new_model_better = True
            # save the new (better) trained model
            # trained_model_id = self.model_repository.generate_unique_trained_model_id(
            #     train_model_request.prediction_job.id
            # )
            serializer = MLflowSerializer(
                trained_models_folder=Path("/data/icarus/visuals/trained_models")
            )
            serializer.save_model(
                model=model,
                pj=prediction_job,
                modelspecs=trained_model_specs,
                report=report,
            )

            # set generic task properties
            train_model_task.training_done = True
            train_model_task.duration = (
                datetime_utc_now() - train_model_task.created
            ).seconds
            self.logger.info(
                "Finished training model successfully",
                duration=train_model_task.duration,
            )

        self.task_controller.update_train_model_task(train_model_task)

    def _train_model_convert_input_data(self, train_model_request):
        # create load feature and add to other features
        load_feature = FeatureModel(name="load", data=train_model_request.load)
        features = [load_feature] + train_model_request.features

        # transpose feature data
        data = []
        for i in range(len(load_feature.data)):
            row = [f.data[i] for f in features]
            data.append(row)

        input_data_dict = {
            "columns": [f.name for f in features],
            "index": train_model_request.index,
            "data": data,
        }
        input_data = pd.DataFrame(**input_data_dict)
        return input_data

    def _train_model_convert_prediction_job(self, train_model_request):
        prediction_job = {
            "name": train_model_request.prediction_job.name,
            "model": train_model_request.prediction_job.model_type,
            "hyper_params": train_model_request.prediction_job.hyper_params,
            "feature_names": train_model_request.prediction_job.feature_names,
        }
        return prediction_job
