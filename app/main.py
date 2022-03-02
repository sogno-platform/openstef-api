"""Main entry point for API"""
# disable some pylint warnings, only for this script because we need the imports in a certain order:
# pylint:disable=wrong-import-position, wrong-import-order, ungrouped-imports

from app.core.initializers import logging

logging.initialize_logging()

import structlog
import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.core.initializers import cors, headers, monitoring, mounting
from app.core.settings import Settings
from app.database import engine, Base
from app.schemas.v1.db_models import TrainModelTask, OptimizeHyperparametersTask

logger = structlog.get_logger(__name__)

# Create and configure new application instance
app = FastAPI(
    title=Settings.app_name,
    description=Settings.app_description,
    version=Settings.app_version,
)

### Create empty tables if not present
Base.metadata.create_all(engine)

# ==================================================================
# SETUP major API versions
# ==================================================================
#
# Import the API routers for each major version.
# Add more if your API supports multiple major versions in parallel.
#
from app.versions.v1 import app as v1

from app.versions.v2 import app as v2

# Then activate enabled API versions:
mounting.mount_api_version(app, v1)
mounting.mount_api_version(app, v2)
# ==================================================================


# ==================================================================
# OPTIONAL modules to include
# ==================================================================
#
# Comment or uncomment the following intialization steps
#  to deactivate/activate a certain feature.
#
# Header constants to include in every response
headers.initialize_metadata_header_middleware(app)

# Liveliness monitoring with Prometheus
# monitoring.initialize_prometheus_middleware(app)

# APM monitoring with Elastic
# monitoring.initialize_apm_middleware(app)

# CORS settings
cors.initialize_cors_middleware(app)
# ==================================================================
# ==================================================================


@app.on_event("startup")
async def startup():
    logger.info("Startup event triggered")
    app.state.started_tasks_train_model = 0
    app.state.started_tasks_optimize_hyperparameters = 0


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown event triggered")

    logger.info("Disposing database engine")
    engine.dispose()


@app.get("/")
def redirect_to_docs():
    """Redirect users to the docs of the default API version (typically the latest)"""
    redirect_url = "/api/v2/docs"  # replace with docs URL or use app.url_path_for()
    return RedirectResponse(url=redirect_url)


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        app,
        host=Settings.api_host,
        port=Settings.api_port,
        log_level=Settings.log_level.lower(),  # Log level should be lowercased for Uvicorn
        log_config=None,  # Required to capture and format Uvicorn's logging
    )
