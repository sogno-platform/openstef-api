"""Prometheus and Elastic APM monitoring middleware"""
import structlog
from starlette_prometheus import PrometheusMiddleware, metrics
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM

from app.core.settings import Settings

logger = structlog.get_logger(__name__)


def initialize_prometheus_middleware(app, endpoint="/metrics"):
    """Start HTTP endpoint for Prometheus monitoring.

    Args:
        app: FastAPI app instance
        endpoint (str): URL at which the metrics should be available
    """
    # only enable if deployed on cluster
    if Settings.deployed:
        logger.info(f'Enabling Prometheus endpoint on: "{endpoint}"')
        app.add_middleware(PrometheusMiddleware)
        app.add_route(endpoint, metrics)


def initialize_apm_middleware(app):
    if Settings.deployed:
        # os.environ["ELASTIC_APM_USE_STRUCTLOG"] = "true"
        logger.info('Enable Elastic APM middleware')
        apm_client = make_apm_client({
            "SERVICE_NAME": Settings.app_name,
            "SECRET_TOKEN": Settings.apm_secret_token,
            "SERVER_URL": Settings.apm_server_url,
            "ENVIRONMENT": Settings.apm_environment
        })
        app.add_middleware(ElasticAPM, client=apm_client)
    else:
        logger.info('Disable Elastic APM middleware when not deployed')
