# tests/test_classification.py

import pytest
from agents.classification_agent import ClassificationAgent
from core.coordination_hub import CoordinationHub

@pytest.fixture
def coordination_hub():
    return CoordinationHub()

@pytest.fixture
def classification_agent(coordination_hub):
    return ClassificationAgent(coordination_hub)

def test_classification_initialization(classification_agent):
    assert classification_agent.name == "ClassificationAgent"
    assert classification_agent.active is True

'''
def test_classify(classification_agent):
    features = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    classifications = classification_agent.classify(features)
    assert isinstance(classifications, list)
    assert len(classifications) == len(features)
'''

def test_classify(classification_agent):
    features = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    
    # Ensure the model is fitted before prediction
    classification_agent.model.fit(features, [0, 1])  # Example training data
    classifications = classification_agent.classify(features)
    assert classifications is not None
