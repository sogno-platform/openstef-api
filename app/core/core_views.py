"""Core endpoints"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def get_api_status():
    """Returns an API health check.

    Includes: API expiry and unit testing
    """
    # TODO: implement API status
    return {"api_status": "API status check not implemented"}


@router.get("/ping")
def get_api_alive():
    """Returns a JSON object. Can be used to check if the API is running.

    Returns:
        JSON object
    """
    return {"api_running": True}
