import pytest
from unittest.mock import MagicMock, patch
from atlas.core.harness import AgentHarness
from atlas.agents.orchestrator import Orchestrator

@patch("atlas.engine.gemini.GeminiEngine.ask")
def test_orchestrator_workflow(mock_ask):
    harness = AgentHarness()
    orchestrator = Orchestrator(harness)
    
    # Mock responses for Orchestrator, Investigator, and Coder
    mock_ask.side_effect = [
        "Plan: Research file X then edit file Y.",  # Orchestrator plan
        "Research: File X contains a bug at line 10.", # Investigator research
        "Result: Successfully fixed bug at line 10 in file Y." # Coder result
    ]
    
    result = orchestrator.plan_and_execute("Fix the bug in file X")
    
    assert "Successfully fixed bug" in result
    assert mock_ask.call_count == 3
