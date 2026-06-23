"""Unit tests verifying Suraksha security logic and compliance limits."""
import pytest
from app.agents.suraksha.anomaly_detector import AnomalyDetector

def test_anomaly_detection():
    detector = AnomalyDetector()
    assert detector.scan_activity() is False
