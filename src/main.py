from core.coordination_hub import CoordinationHub
from agents.data_collection_agent import DataCollectionAgent
from agents.feature_extraction_agent import FeatureExtractionAgent
from agents.classification_agent import ClassificationAgent
from agents.response_agent import ResponseAgent
from agents.system_optimizer_agent import SystemOptimizerAgent
from agents.security_auditor_agent import SecurityAuditorAgent
from agents.health_monitoring_agent import HealthMonitoringAgent
from utils.logger import setup_logging
import logging
import multiprocessing
import time

# Configure global logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_agent(agent):
    """
    Function to start each agent by running their run() method.
    This avoids using threading and relies on multiprocessing instead.
    """
    agent.run()

def main():
    """
    Entry point for the BustedURL system.
    Initializes all agents and starts the decentralized coordination hub.
    """
    # Initialize logging
    setup_logging()

    logger.info("BustedURL application started")
    try:
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

        # Create processes for each agent and directly run the `run()` method
        processes = [
            multiprocessing.Process(target=run_agent, args=(data_collection_agent,)),
            multiprocessing.Process(target=run_agent, args=(feature_extraction_agent,)),
            multiprocessing.Process(target=run_agent, args=(classification_agent,)),
            multiprocessing.Process(target=run_agent, args=(response_agent,)),
            multiprocessing.Process(target=run_agent, args=(system_optimizer_agent,)),
            multiprocessing.Process(target=run_agent, args=(security_auditor_agent,)),
            multiprocessing.Process(target=run_agent, args=(health_monitoring_agent,))
        ]
    
        # Start all processes
        for process in processes:
            process.start()
    
        # Monitor agents and handle any failures or restarts
        try:
            while True:
                hub.monitor_agents()
                time.sleep(5)  # Adjust the monitoring interval as needed
        except KeyboardInterrupt:
            print("Shutting down BustedURL system...")
            hub.stop()
            # Terminate all agent processes
            for process in processes:
                process.terminate()
                process.join()
            print("All agents have been stopped. System exited successfully.")
        logger.info("All agents started successfully")
    except Exception as e:
        logger.error(f"An error occurred in the main execution: {e}")
        raise


if __name__ == "__main__":
    main()
