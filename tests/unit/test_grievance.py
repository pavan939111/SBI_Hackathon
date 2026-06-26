"""
Unit tests validating Grievance lodging endpoint and model properties.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.models.grievance import Grievance
from app.api.v1.grievance import create_grievance, GrievanceCreate

def test_grievance_model_instantiation():
    g = Grievance(
        customer_id="RAJU_7823",
        category="YONO App",
        details="Unable to log in to YONO App."
    )
    assert g.customer_id == "RAJU_7823"
    assert g.category == "YONO App"
    assert g.details == "Unable to log in to YONO App."
    assert g.status == "open"

@pytest.mark.asyncio
async def test_create_grievance_endpoint():
    db_session = MagicMock()
    db_session.add = MagicMock()
    db_session.commit = AsyncMock()
    db_session.refresh = AsyncMock()
    
    payload = GrievanceCreate(
        customer_id="RAJU_7823",
        category="Authentication",
        details="OTP is not being delivered."
    )
    
    response = await create_grievance(payload, db=db_session)
    assert response["status"] == "open"
    assert "registered successfully" in response["message"]
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
