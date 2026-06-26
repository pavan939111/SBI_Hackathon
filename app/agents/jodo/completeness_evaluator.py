"""
Completeness Evaluator calculating Jodo profile scores and prioritizing missing gaps.
"""
from typing import Dict, Any, List, Tuple

class CompletenessEvaluator:
    """
    Evaluates customer profile records to produce 0-100 completeness score 
    and identify missing details.
    """
    
    # Priority rank: higher-impact gaps resolved first
    PRIORITY_FIELDS = [
        "kyc_occupation",       # 25 pts
        "aadhaar_linked",       # 30 pts
        "nominee_name",          # 15 pts
    ]

    def evaluate(self, customer: Dict[str, Any]) -> Tuple[int, List[str]]:
        """
        Calculates Jodo score and returns list of prioritized missing fields.
        """
        score = 0
        missing_fields = []
        
        # 1. Contact details current (10 pts)
        if customer.get("phone_number"):
            score += 10
        else:
            missing_fields.append("phone_number")
            
        # 2. Aadhaar seeded (30 pts)
        if customer.get("aadhaar_linked") is True:
            score += 30
        else:
            missing_fields.append("aadhaar_linked")
            
        # 3. Occupation flag current (25 pts)
        occupation = customer.get("kyc_occupation")
        if occupation and occupation.lower() not in ["unknown", "missing", ""]:
            score += 25
        else:
            missing_fields.append("kyc_occupation")
            
        # 4. Nominee added (15 pts)
        if customer.get("nominee_name"):
            score += 15
        else:
            missing_fields.append("nominee_name")
            
        # 5. Active transaction pattern (20 pts) - read-only proxy
        # If customer has a transaction history already present, reward 20 pts
        if customer.get("has_active_transactions") is True or customer.get("dms_level", 0) >= 2:
            score += 20
            
        # Sort missing fields by priority
        prioritized_missing = [f for f in self.PRIORITY_FIELDS if f in missing_fields]
        for f in missing_fields:
            if f not in prioritized_missing:
                prioritized_missing.append(f)
                
        return score, prioritized_missing
