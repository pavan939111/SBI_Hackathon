"""
Unit tests validating Jodo profile completeness score calculations and priority resolver.
"""
import pytest
from app.agents.jodo.completeness_evaluator import CompletenessEvaluator

def test_jodo_completeness_empty():
    evaluator = CompletenessEvaluator()
    profile = {
        "phone_number": None,
        "aadhaar_linked": False,
        "kyc_occupation": "Unknown",
        "nominee_name": "",
        "dms_level": 0
    }
    score, missing = evaluator.evaluate(profile)
    assert score == 0
    # Prioritized fields should check occupation first, then Aadhaar, then nominee
    assert missing == ["kyc_occupation", "aadhaar_linked", "nominee_name", "phone_number"]

def test_jodo_completeness_partially_completed():
    evaluator = CompletenessEvaluator()
    profile = {
        "phone_number": "+919400000000", # 10 pts
        "aadhaar_linked": False,
        "kyc_occupation": "farmer",       # 25 pts
        "nominee_name": "",
        "dms_level": 1
    }
    score, missing = evaluator.evaluate(profile)
    # 10 (phone) + 25 (occupation) = 35 pts
    assert score == 35
    assert "aadhaar_linked" in missing
    assert "nominee_name" in missing

def test_jodo_completeness_full_conversational_updates():
    evaluator = CompletenessEvaluator()
    profile = {
        "phone_number": "+919400000000", # 10 pts
        "aadhaar_linked": True,          # 30 pts
        "kyc_occupation": "farmer",       # 25 pts
        "nominee_name": "Sita Reddy",     # 15 pts
        "dms_level": 1
    }
    score, missing = evaluator.evaluate(profile)
    # 10 + 30 + 25 + 15 = 80 pts (conversational max without transaction pattern)
    assert score == 80
    assert len(missing) == 0

def test_jodo_completeness_with_transactions():
    evaluator = CompletenessEvaluator()
    profile = {
        "phone_number": "+919400000000", # 10 pts
        "aadhaar_linked": True,          # 30 pts
        "kyc_occupation": "farmer",       # 25 pts
        "nominee_name": "Sita Reddy",     # 15 pts
        "dms_level": 2                   # unlocks active transaction pattern (20 pts)
    }
    score, missing = evaluator.evaluate(profile)
    # 10 + 30 + 25 + 15 + 20 = 100 pts (maximum target score reached)
    assert score == 100
    assert len(missing) == 0
