# tests/test_security_auditor.py

import pytest
from agents.security_auditor_agent import SecurityAuditorAgent
from core.coordination_hub import CoordinationHub

@pytest.fixture
def coordination_hub():
    return CoordinationHub()

@pytest.fixture
def security_auditor_agent(coordination_hub):
    return SecurityAuditorAgent(coordination_hub)

def test_security_auditor_initialization(security_auditor_agent):
    assert security_auditor_agent.name == "SecurityAuditorAgent"
    assert security_auditor_agent.active is True

def test_audit_security(security_auditor_agent):
    security_auditor_agent.audit_security()
    # Check MongoDB or logs for stored vulnerabilities
