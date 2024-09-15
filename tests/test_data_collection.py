# tests/test_data_collection.py

import pytest
from agents.data_collection_agent import DataCollectionAgent
from core.coordination_hub import CoordinationHub

@pytest.fixture
def coordination_hub():
    return CoordinationHub()

@pytest.fixture
def data_collection_agent(coordination_hub):
    return DataCollectionAgent(coordination_hub)

def test_data_collection_initialization(data_collection_agent):
    assert data_collection_agent.name == "DataCollectionAgent"
    assert data_collection_agent.active is True

def test_collect_urls(data_collection_agent):
    urls = data_collection_agent.collect_urls()
    assert isinstance(urls, list)
    assert all(isinstance(url, str) for url in urls)
