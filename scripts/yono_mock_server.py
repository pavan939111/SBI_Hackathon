"""
Mock server simulating SBI YONO frontend API endpoints to support local testing.
"""
from fastapi import FastAPI, Body

app = FastAPI(title="YONO Mock API Server", version="0.1.0")

# Local in-memory state tracking to simulate updates
MOCK_PROFILE = {
    "customer_id": "RAJU_7823",
    "name": "Raju Reddy",
    "mobile": "+919400000000",
    "dms_level": 1,
    "kyc_occupation": "Unknown",
    "aadhaar_linked": False,
    "nominee_name": "",
    "nominee_relation": "",
    "profile_score": 35
}

@app.get("/profile")
def get_profile():
    return MOCK_PROFILE

@app.post("/profile/declare-occupation")
def declare_occupation(occupation: str = Body(..., embed=True)):
    MOCK_PROFILE["kyc_occupation"] = occupation
    MOCK_PROFILE["profile_score"] = min(100, MOCK_PROFILE["profile_score"] + 25)
    return {"status": "success", "profile": MOCK_PROFILE}

@app.post("/profile/request-aadhaar-link")
def request_aadhaar_link(aadhaar: str = Body(..., embed=True)):
    # Simulates request submission, set to True for mock verification
    MOCK_PROFILE["aadhaar_linked"] = True
    MOCK_PROFILE["profile_score"] = min(100, MOCK_PROFILE["profile_score"] + 30)
    return {"status": "request_submitted", "profile": MOCK_PROFILE}

@app.get("/balance")
def get_balance():
    return {"account_number": "XXXX7823", "balance": 18400.0}

@app.get("/transactions")
def get_transactions():
    return {
        "transactions": [
            {"date": "2026-06-01", "amount": -1500, "category": "agri_input_purchase"},
            {"date": "2026-06-15", "amount": 25000, "category": "crop_sale_credit"}
        ]
    }

@app.get("/products-held")
def get_products_held():
    return {"active_loans": [], "fds": [], "rds": []}

@app.get("/appointment-slots")
def get_slots():
    return {"slots": ["Tuesday 10:00am", "Wednesday 11:30am"]}

@app.get("/document-vault")
def get_vault():
    return {"documents": ["land_records_verified", "kyc_aadhaar"]}

