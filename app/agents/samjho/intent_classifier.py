"""
Classification models mapping conversational content to semantic target keys.
"""
class IntentClassifier:
    def classify(self, text: str) -> str:
        """Determines the conversation intent of the customer request."""
        clean_text = text.lower()
        if "loan" in clean_text or "kcc" in clean_text:
            return "loan_inquiry"
        if "appointment" in clean_text or "branch" in clean_text:
            return "appointment"
        if "fraud" in clean_text or "block" in clean_text or "scam" in clean_text:
            return "fraud_alert"
        return "general_query"
