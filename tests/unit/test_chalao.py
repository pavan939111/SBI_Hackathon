"""Unit tests verifying Chalao recovery flow and UI navigations."""
import pytest
from app.agents.chalao.yono_navigator import YONONavigator

def test_navigator_steps():
    navigator = YONONavigator()
    steps = navigator.get_steps("KCC_001")
    assert len(steps) > 0
    assert "Loans" in steps[1]
