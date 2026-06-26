"""
API endpoints for lodging customer complaints and grievances.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.api.dependencies import get_db_session
from app.models.grievance import Grievance

router = APIRouter()

class GrievanceCreate(BaseModel):
    customer_id: Optional[str] = None
    category: str
    details: str

class GrievanceResponse(BaseModel):
    id: str
    status: str
    message: str

@router.post("", response_model=GrievanceResponse, status_code=status.HTTP_201_CREATED)
async def create_grievance(payload: GrievanceCreate, db: AsyncSession = Depends(get_db_session)):
    """Logs a new customer grievance request to the database."""
    if not payload.category or not payload.details:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category and details are required to file a grievance."
        )
        
    grievance = Grievance(
        customer_id=payload.customer_id,
        category=payload.category,
        details=payload.details
    )
    
    db.add(grievance)
    await db.commit()
    await db.refresh(grievance)
    
    return {
        "id": grievance.id,
        "status": grievance.status,
        "message": "Grievance registered successfully in mock CRM."
    }
