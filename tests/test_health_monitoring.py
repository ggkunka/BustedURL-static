# tests/test_health_monitoring.py

import pytest
from core.coordination_hub import CoordinationHub
from agents.health_monitoring_agent import HealthMonitoringAgent

@pytest.fixture
def coordination_hub():
    return CoordinationHub()

@pytest.fixture
def health_monitoring_agent(coordination_hub):
    agent = HealthMonitoringAgent(coordination_hub)
    agent.start()  # Start the thread when the fixture is created
    return agent

def test_monitor_health(health_monitoring_agent):
    # Wait for a short period to allow some data to be collected
    import time
    time.sleep(2)  # Wait for 2 seconds to allow monitoring threads to collect data

    # Example assertion to check that the agent is active
    assert health_monitoring_agent.cpu_gauge is not None
    assert health_monitoring_agent.memory_gauge is not None
