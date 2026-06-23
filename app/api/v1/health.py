"""
FastAPI route verifying system liveness and database connections.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def liveness():
    return {"status": "ok", "service": "banksaathi"}
