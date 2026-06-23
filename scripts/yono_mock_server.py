"""
Mock server simulating SBI YONO frontend API endpoints to support local testing.
"""
from fastapi import FastAPI

app = FastAPI(title="YONO Mock API Server", version="0.1.0")

@app.get("/profile")
def get_profile():
    return {
        "customer_id": "RAJU_7823",
        "name": "Raju Reddy",
        "mobile": "+919400000000",
        "dms_level": 1,
        "kyc_occupation": "farmer"
    }

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
