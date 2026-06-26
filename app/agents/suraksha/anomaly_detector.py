"""
Heuristic analysis components measuring transaction anomalies.
"""
class AnomalyDetector:
    def scan_activity(self, message: str = "") -> bool:
        """Validates message patterns to check for anomalies or fraud warnings."""
        clean_msg = message.lower()
        suspicious_keywords = ["scam", "otp", "pin", "unauthorized", "stolen", "block my account"]
        for key in suspicious_keywords:
            if key in clean_msg:
                return True
        return False


