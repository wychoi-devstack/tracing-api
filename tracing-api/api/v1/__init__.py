from fastapi import APIRouter
from . import tracing

api_router = APIRouter()
api_router.include_router(tracing.router, tags=["Tracing"])
