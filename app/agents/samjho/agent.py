"""
Samjho agent: parsing languages, identifying intents, and assessing DPDP consent.
"""
from app.agents.state import AgentState
from app.agents.samjho.intent_classifier import IntentClassifier
from app.agents.samjho.language_detector import LanguageDetector

async def samjho_node(state: AgentState) -> AgentState:
    """Classifies user input, extracts parameters and updates system state."""
    text_content = state["messages"][-1]["content"] if state["messages"] else ""
    
    lang_detector = LanguageDetector()
    intent_classifier = IntentClassifier()
    
    state["language"] = lang_detector.detect(text_content)
    state["intent"] = intent_classifier.classify(text_content)
    
    # Defaults low risk tier initially
    state["risk_tier"] = 1
    return state
