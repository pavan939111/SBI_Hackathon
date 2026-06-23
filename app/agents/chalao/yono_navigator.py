"""
Navigation mapping configuration representing pre-defined YONO UI steps.
"""
from typing import List

class YONONavigator:
    def get_steps(self, scheme_id: str) -> List[str]:
        """Produces navigation directives for the given target scheme."""
        if scheme_id == "KCC_001":
            return [
                "Open YONO App",
                "Navigate to 'Loans' menu panel",
                "Select 'Kisan Credit Card (KCC)' option",
                "Confirm pre-populated account information details"
            ]
        return ["Open YONO App", "Navigate to 'Services' menu option"]
