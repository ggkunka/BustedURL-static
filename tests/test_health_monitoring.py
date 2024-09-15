# tests/test_health_monitoring.py

import pytest
from agents.health_monitoring_agent import HealthMonitoringAgent
from core.coordination_hub import CoordinationHub

@pytest.fixture
def coordination_hub():
    return CoordinationHub()

@pytest.fixture
def health_monitoring_agent(coordination_hub):
    return HealthMonitoringAgent(coordination_hub)

def test_health_monitoring_initialization(health_monitoring_agent):
    assert health_monitoring_agent.name == "HealthMonitoringAgent"
    assert health_monitoring_agent.active is True

def test_monitor_health(health_monitoring_agent):
    health_monitoring_agent.monitor_health()
    # Check Prometheus metrics for updates
