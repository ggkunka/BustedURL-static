# tests/test_feature_extraction.py

import pytest
from agents.feature_extraction_agent import FeatureExtractionAgent
from core.coordination_hub import CoordinationHub

@pytest.fixture
def coordination_hub():
    return CoordinationHub()

@pytest.fixture
def feature_extraction_agent(coordination_hub):
    return FeatureExtractionAgent(coordination_hub)

def test_feature_extraction_initialization(feature_extraction_agent):
    assert feature_extraction_agent.name == "FeatureExtractionAgent"
    assert feature_extraction_agent.active is True

def test_extract_features(feature_extraction_agent):
    urls = ["http://example.com", "https://test.com"]
    features = feature_extraction_agent.extract_features(urls)
    assert isinstance(features, list)
    assert len(features) == len(urls)
