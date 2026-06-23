"""
Main FastAPI server application setup and router hooks.
"""
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import CorrelationIDMiddleware
from app.db.migration_runner import run_migrations

setup_logging()

app = FastAPI(
    title="BankSaathi Backend API",
    description="Agentic AI Companion platform for SBI Customers",
    version="0.1.0"
)

# Register Middleware for request tracing
app.add_middleware(CorrelationIDMiddleware)

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Run SQL database schema bootstrap migrations on startup
    await run_migrations()

@app.get("/")
async def root():
    return {"name": "BankSaathi API", "status": "active"}

