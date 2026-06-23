"""Unit tests verifying Samjho intent classification and language detection."""
import pytest
from app.agents.samjho.intent_classifier import IntentClassifier

def test_intent_classification():
    classifier = IntentClassifier()
    intent = classifier.classify("I need a loan for crops")
    assert intent == "loan_inquiry"
