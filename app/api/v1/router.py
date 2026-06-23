"""
Combines health check, admin operations and webhook hooks.
"""
from fastapi import APIRouter
from app.api.v1 import webhook, health, admin

api_router = APIRouter()
api_router.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
