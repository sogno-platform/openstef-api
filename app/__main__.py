import uvicorn
from app import main
from app.core.settings import Settings

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        main.app,
        host=Settings.api_host,
        port=Settings.api_port,
        log_level=Settings.log_level.lower(),  # Log level should be lowercased for Uvicorn
        log_config=None,  # Required to capture and format Uvicorn's logging
    )