from fastapi import FastAPI
from .core.router import router as core_router
from .dashboard.router import router as dashboard_router

app = FastAPI(
    title="Lab3 FastAPI Project",
    description="Навчальний проєкт з модульною структурою (FastAPI).",
    version="1.0.0",
)

@app.get("/", tags=["root"])
def root():
    return {"message": "Hello from LR3!", "docs": "/docs", "redoc": "/redoc"}

app.include_router(core_router)
app.include_router(dashboard_router)
