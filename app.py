import threading
import time
import logging
import pika
import pymongo

from agents.data_collection import DataCollectionAgent
from agents.feature_extraction import FeatureExtractionAgent
from agents.classification import ClassificationAgent
from agents.response import ResponseAgent
from agents.system_optimizer import SystemOptimizerAgent
from agents.security_auditor import SecurityAuditorAgent
from agents.health_monitoring import HealthMonitoringAgent
from utils.logger import setup_logging

# Setup logging
setup_logging()

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["bustedurl"]
collection_urls = db["urls"]

# RabbitMQ Configuration
rabbitmq_host = 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue='url_queue')

def run_agent(agent):
    """
    Function to run an agent in a separate thread.
    """
    agent.run()

def main():
    # Initialize agents with direct message-passing capabilities
    data_collection_agent = DataCollectionAgent(channel, collection_urls)
    feature_extraction_agent = FeatureExtractionAgent(channel)
    classification_agent = ClassificationAgent(channel)
    response_agent = ResponseAgent(channel)
    system_optimizer_agent = SystemOptimizerAgent(channel)
    security_auditor_agent = SecurityAuditorAgent(channel)
    health_monitoring_agent = HealthMonitoringAgent(channel)

    # Start agents in separate threads
    threads = []
    agents = [
        data_collection_agent, feature_extraction_agent, classification_agent,
        response_agent, system_optimizer_agent, security_auditor_agent, health_monitoring_agent
    ]

    for agent in agents:
        thread = threading.Thread(target=run_agent, args=(agent,))
        threads.append(thread)
        thread.start()
        logging.info(f"{agent.__class__.__name__} started.")

    # Main application loop
    try:
        while True:
            # Monitor agents and perform tasks
            time.sleep(10)  # Replace with actual task or monitoring logic
            logging.info("Monitoring agents...")
    except KeyboardInterrupt:
        logging.info("Shutting down BustedURL...")
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()
