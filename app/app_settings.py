"""App and API settings"""
from pathlib import Path
from typing import List

from pydantic import AnyUrl, BaseSettings, EmailStr, Field
from pydantic.types import SecretStr


class AppSettings(BaseSettings):
    """Global app and API settings.

    Define your default values here. Values can be overriden by ENV variables with
    the same name.

    In the code, you can access these variables like this:
        >>> from app.core.settings import Settings
        >>> print(Settings.app_name)
        template-kubernetes-fastapi
    """

    # APP settings
    app_name: str = Field(
        "icarus-openstf-api",
        description="App name, typically the same as the deployment name",
    )
    app_description: str = Field(
        "This API exposes the main machine learning pipelines of the openstef library",
        description="What does the app do?",
    )
    app_maintainer: str = Field(
        "Korte termijn prognoses",
        description="The maintainer of this app that should be contacted in case of questions and problems",
    )
    app_maintainer_email: EmailStr = Field(
        "korte.termijn.prognoses@alliander.com",
        description="The maintainer's email adress",
    )
    app_version: str = Field(
        "0.2.0",
        description="The app's version. Note that this is not necessarily the same as the API version.",
    )

    # API Settings
    api_host: str = Field("127.0.0.1", description="Host identifier for listening.")
    api_port: int = Field(
        8000, description="Port to which the web server must bind.", env="PORT"
    )

    api_enable_core_endpoints: bool = Field(
        True, description="Enables core endpoints: /status and /ping"
    )
    api_cors_allowed_origins: List[AnyUrl] = Field(
        [],
        description="Enables CORS for the allowed origins; a list of strings each corresponding to a host.",
    )

    # Trained models repository
    trained_models_folder: Path = Field(
        Path("trained-models"),
        description="The directory which will be used to store and retrieve trained models from",
    )
    trained_model_reports_folder: Path = Field(
        Path("trained-models"),
        description="The directory which will be used to store and retrieve trained model reports from",
    )

    # Redis settings
    redis_host:str = "localhost"
    redis_port:int = 6379
    redis_username = "default"
    redis_password:SecretStr = "testpw"

    # AMQP settings
    amqp_host:str = "localhost"
    amqp_port:int = 5672
    amqp_username:str = "user"
    amqp_password:SecretStr = "testpw"
    amqp_exchange:str = "forecastingjobs"

    # # MySQL settings
    # mysql_username: str = ""
    # mysql_host: str = ""
    # mysql_port: int = 3306
    # mysql_password: SecretStr = ""
    # mysql_database: str = ""
    # # InfluxDB settings (used to get predictors)
    # influxdb_username: str = ""
    # influxdb_password: SecretStr = ""
    # influxdb_host: str = ""
    # influxdb_port: int = 8086

    # APM settings
    apm_secret_token: str = Field("", description="The APM secret token")
    apm_server_url: str = Field(
        "http://localhost:8200", description="The url of the Elastic instance"
    )
    apm_environment: str = Field(
        "development",
        description="The Elastic APM environment. Usually 'production', 'acceptance', 'test' or 'development'",
    )

    max_background_tasks: int = Field(
        2, description="The maximum number of background tasks per endpoint."
    )

    # DEPLOYMENT and ENVIRONMENT Settings
    log_level: str = "INFO"
    log_json_output: bool = Field(
        False, description="Use JSON log output or plain text"
    )

    deployed: bool = Field(
        False,
        description="Whether the app is running as deployment on a cluster (OpenShift/EKS) or locally.",
    )


class DeployedAppSettings(AppSettings):
    """Define default values if the app is deployed on OpenShift/EKS."""

    api_host: str = Field("0.0.0.0", description="Host identifier for listening.")
    deployed: bool = Field(
        True,
        description="Whether the app is running as deployment on a cluster (OpenShift/EKS).",
    )
    log_json_output: bool = Field(True, description="Use JSON log output or plain text")

    trained_models_folder: Path = Field(
        Path("/data/icarus/visuals/trained_models"),
        description="The directory which will be used to store and retrieve trained models from",
    )
    trained_model_reports_folder: Path = Field(
        Path("/data/icarus/visuals/trained_models"),
        description="The directory which will be used to store and retrieve trained model reports from",
    )


class LocalAppSettings(AppSettings):
    """Define default values if the app runs locally."""
