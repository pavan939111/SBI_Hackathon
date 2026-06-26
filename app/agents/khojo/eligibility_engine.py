"""
Rule engines executing criteria validation on targeted banking products.
"""
from typing import List, Dict, Any
from app.agents.khojo.scheme_loader import SchemeLoader

class EligibilityEngine:
    def __init__(self):
        self.loader = SchemeLoader()

    def evaluate_customer_eligibility(self, profile: Dict[str, Any]) -> List[str]:
        """Calculates matching score metrics for registered packages based on rules."""
        schemes = self.loader.load_local_schemes()
        matched = []
        
        occupation = profile.get("kyc_occupation", "Unknown").lower()
        aadhaar_linked = profile.get("aadhaar_linked", False)
        
        for scheme in schemes:
            rules = scheme.get("eligibility_rules", {})
            
            # 1. Occupation check
            allowed_occupations = [o.lower() for o in rules.get("occupation_flags", [])]
            if "any" not in allowed_occupations and occupation not in allowed_occupations:
                continue
                
            # 2. Aadhaar link check (if required by rules)
            if rules.get("requires_land_records", False) and not aadhaar_linked:
                continue
                
            matched.append(scheme["scheme_id"])
            
        return matched

