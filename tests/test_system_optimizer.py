# tests/test_system_optimizer.py

import pytest
from agents.system_optimizer_agent import SystemOptimizerAgent
from core.coordination_hub import CoordinationHub

@pytest.fixture
def coordination_hub():
    return CoordinationHub()

@pytest.fixture
def system_optimizer_agent(coordination_hub):
    return SystemOptimizerAgent(coordination_hub)

def test_system_optimizer_initialization(system_optimizer_agent):
    assert system_optimizer_agent.name == "SystemOptimizerAgent"
    assert system_optimizer_agent.active is True

def test_optimize_system(system_optimizer_agent):
    system_optimizer_agent.optimize_system()
    # Check logs or other methods to verify optimization actions
