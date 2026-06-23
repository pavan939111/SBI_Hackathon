"""
Pydantic schemas validating output results of scheme evaluations.
"""
from pydantic import BaseModel
from typing import List

class EligibilityResult(BaseModel):
    scheme_id: str
    name: str
    eligible: bool
    matching_score: float
    reasons: List[str]
