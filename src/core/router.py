from fastapi import APIRouter
from datetime import datetime
import platform

from .models import HealthResponse, TimeResponse

router = APIRouter(prefix="/common", tags=["common"])

@router.get("/healthcheck", response_model=HealthResponse, summary="Healthcheck")
def healthcheck():
    return {"status": "ok", "message": "Service is running"}

@router.get("/time", response_model=TimeResponse, summary="Get server time")
def get_time():
    return {"server_time": datetime.utcnow().isoformat() + "Z"}

@router.get("/info", summary="System info")  
def info():
    return {
        "python": platform.python_version(),
        "system": platform.system(),
        "release": platform.release(),
    }
