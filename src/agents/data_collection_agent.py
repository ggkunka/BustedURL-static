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
from utils.data_cleaner import clean_data  # Import the data cleaning function
import logging
import multiprocessing
import time
from multiprocessing import Queue
import os

# File paths for the raw and cleaned data
RAW_DATA_PATH = 'data/raw/raw_data.csv'
CLEANED_DATA_PATH = 'data/processed/cleaned_data.csv'

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
    
    # Step 1: Clean the raw data
    logger.info(f"Cleaning data from {RAW_DATA_PATH} and saving it to {CLEANED_DATA_PATH}")
    try:
        if not os.path.exists(RAW_DATA_PATH):
            raise FileNotFoundError(f"Raw data file {RAW_DATA_PATH} not found")
        
        clean_data(RAW_DATA_PATH, CLEANED_DATA_PATH)
        logger.info(f"Data cleaning completed successfully, saved to {CLEANED_DATA_PATH}")
    except Exception as e:
        logger.error(f"An error occurred during data cleaning: {e}")
        return  # Exit if data cleaning fails

    # Step 2: Start agents
    try:
        # Initialize the Coordination Hub (if still needed for logging, monitoring, etc.)
        hub = CoordinationHub()

        # Create Queues for inter-process communication
        input_queue = Queue()
        output_queue = Queue()

        # Initialize Agents with input_queue and output_queue
        data_collection_agent = DataCollectionAgent(input_queue, output_queue)
        feature_extraction_agent = FeatureExtractionAgent(input_queue, output_queue)
        classification_agent = ClassificationAgent(input_queue, output_queue)
        response_agent = ResponseAgent(input_queue, output_queue)
        system_optimizer_agent = SystemOptimizerAgent(input_queue, output_queue)
        security_auditor_agent = SecurityAuditorAgent(input_queue, output_queue)
        health_monitoring_agent = HealthMonitoringAgent(input_queue, output_queue)
    
        # Start the Coordination Hub (if necessary)
        hub.start()

        # Create processes for each agent and directly run the `run()` method
        processes = [
            multiprocessing.Process(target=run_agent, args=(data_collection_agent,)),
            multiprocessing.Process(target=run_agent, args=(feature_extraction_agent,)),
            multiprocessing.Process(target=run_agent, args=(classification_agent,)),
            multiprocessing.Process(target=run_agent, args=(response_agent,)),
            multiprocessing.Process(target=run_agent, args=(system_optimizer_agent,)),
            multiprocessing.Process(target=run_agent, args=(security_auditor_agent,)),
            multiprocessing.Process(target=run_agent, args=(health_monitoring_agent,)),
        ]
    
        # Start all processes
        for process in processes:
            process.start()
    
        # Monitor agents and handle any failures or restarts
        try:
            while True:
                # Monitor agent status or handle inter-process communication here
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
