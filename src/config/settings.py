# config/settings.py

"""
Global configuration settings for the BustedURL project.
"""

# General Settings
PROJECT_NAME = "BustedURL"
LOG_LEVEL = "INFO"
LOG_FILE_PATH = "logs/bustedurl.log"

# Database Settings
MONGODB_URI = "mongodb://localhost:27017"
MONGODB_DB_NAME = "bustedurl_db"

# Message Broker Settings (RabbitMQ)
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE_NAME = "agent_communication"

# Prometheus Monitoring Settings
PROMETHEUS_PORT = 8000

# Model Paths
MODEL_SAVE_PATH = "models/"
MODEL_NAME = "url_classifier.pkl"

# Security Settings
ENCRYPTION_KEY = b'your-generated-encryption-key-here'  # Replace with your generated encryption key

# Other Settings
DATA_COLLECTION_INTERVAL = 60  # Time interval in seconds for data collection
SYSTEM_OPTIMIZATION_INTERVAL = 30  # Time interval in seconds for system optimization
SECURITY_AUDIT_INTERVAL = 120  # Time interval in seconds for security audits
HEALTH_MONITORING_INTERVAL = 15  # Time interval in seconds for health monitoring

