from fastapi import APIRouter

from app.api.health import endpoint as health
from app.api.user import endpoint as user

api_router = APIRouter()

api_router.include_router(health.router, include_in_schema=False)
api_router.include_router(user.router, include_in_schema=False)
