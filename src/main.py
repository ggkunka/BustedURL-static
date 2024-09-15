# main.py

from core.coordination_hub import CoordinationHub
from agents.data_collection_agent import DataCollectionAgent
from agents.feature_extraction_agent import FeatureExtractionAgent
from agents.classification_agent import ClassificationAgent
from agents.response_agent import ResponseAgent
from agents.system_optimizer_agent import SystemOptimizerAgent
from agents.security_auditor_agent import SecurityAuditorAgent
from agents.health_monitoring_agent import HealthMonitoringAgent
from utils.logger import setup_logging

def main():
    """
    Entry point for the BustedURL system.
    Initializes all agents and starts the decentralized coordination hub.
    """
    # Initialize logging
    setup_logging()

    # Initialize the Coordination Hub
    hub = CoordinationHub()

    # Initialize Agents
    data_collection_agent = DataCollectionAgent(hub)
    feature_extraction_agent = FeatureExtractionAgent(hub)
    classification_agent = ClassificationAgent(hub)
    response_agent = ResponseAgent(hub)
    system_optimizer_agent = SystemOptimizerAgent(hub)
    security_auditor_agent = SecurityAuditorAgent(hub)
    health_monitoring_agent = HealthMonitoringAgent(hub)

    # Register Agents with the Coordination Hub
    hub.register_agent(data_collection_agent)
    hub.register_agent(feature_extraction_agent)
    hub.register_agent(classification_agent)
    hub.register_agent(response_agent)
    hub.register_agent(system_optimizer_agent)
    hub.register_agent(security_auditor_agent)
    hub.register_agent(health_monitoring_agent)

    # Start the Coordination Hub
    hub.start()

    # Start all agents
    data_collection_agent.start()
    feature_extraction_agent.start()
    classification_agent.start()
    response_agent.start()
    system_optimizer_agent.start()
    security_auditor_agent.start()
    health_monitoring_agent.start()

    # Monitor agents and handle any failures or restarts
    try:
        while True:
            hub.monitor_agents()
    except KeyboardInterrupt:
        print("Shutting down BustedURL system...")
        hub.stop()
        print("All agents have been stopped. System exited successfully.")

if __name__ == "__main__":
    main()