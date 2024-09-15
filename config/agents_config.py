# config/agents_config.py

"""
Configuration settings specific to each agent in the BustedURL project.
"""

from config.settings import *

# Data Collection Agent Settings
DATA_COLLECTION_AGENT_CONFIG = {
    "enabled": True,
    "data_sources": [
        "https://example.com/urls",
        "https://another-source.com/feed"
    ],
    "scraping_interval": DATA_COLLECTION_INTERVAL,
    "api_keys": {
        "source1": "your-api-key-here",
        "source2": "another-api-key"
    }
}

# Feature Extraction Agent Settings
FEATURE_EXTRACTION_AGENT_CONFIG = {
    "enabled": True,
    "model_name": "all-MiniLM-L6-v2",  # Name of the SentenceTransformer model
    "batch_size": 32,
}

# Classification Agent Settings
CLASSIFICATION_AGENT_CONFIG = {
    "enabled": True,
    "model_path": MODEL_SAVE_PATH + MODEL_NAME,
    "retrain_on_start": False,
}

# Response Agent Settings
RESPONSE_AGENT_CONFIG = {
    "enabled": True,
    "alert_methods": ["email", "sms"],  # Methods to send alerts for malicious URLs
    "encryption_key": ENCRYPTION_KEY,
}

# System Optimizer Agent Settings
SYSTEM_OPTIMIZER_AGENT_CONFIG = {
    "enabled": True,
    "optimization_interval": SYSTEM_OPTIMIZATION_INTERVAL,
    "cpu_threshold": 80,  # CPU usage percentage threshold for optimization
    "memory_threshold": 75,  # Memory usage percentage threshold for optimization
}

# Security Auditor Agent Settings
SECURITY_AUDITOR_AGENT_CONFIG = {
    "enabled": True,
    "audit_interval": SECURITY_AUDIT_INTERVAL,
    "vulnerability_sources": ["owasp", "nvd"],  # Example sources for vulnerability checks
}

# Health Monitoring Agent Settings
HEALTH_MONITORING_AGENT_CONFIG = {
    "enabled": True,
    "monitoring_interval": HEALTH_MONITORING_INTERVAL,
    "prometheus_port": PROMETHEUS_PORT,
}

