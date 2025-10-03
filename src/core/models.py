from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    message: str

class TimeResponse(BaseModel):
    server_time: str
