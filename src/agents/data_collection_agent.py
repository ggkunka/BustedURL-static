# agents/data_collection_agent.py

from multiprocessing import Process
import logging
import time
import requests
from bs4 import BeautifulSoup
from utils.logger import get_logger

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataCollectionAgent(Process):  # Use Process instead of Thread
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.name = "DataCollectionAgent"
        self.active = True
        self.logger = get_logger(self.name)

    def run(self):
        """
        Continuously collects URLs from various sources and sends them to the FeatureExtractionAgent.
        """
        self.logger.info(f"{self.name} started.")
        while self.active:
            try:
                urls = self.collect_urls()
                if urls:
                    self.hub.send_message(self.name, "FeatureExtractionAgent", {"urls": urls})
                time.sleep(60)  # Collect URLs every 60 seconds
            except Exception as e:
                self.logger.error(f"Error in {self.name}: {e}")

    def collect_urls(self):
        """
        Collects URLs from web sources using BeautifulSoup.
        """
        self.logger.info("Starting data collection...")
        try:
            urls = []
            response = requests.get("https://example.com/urls")  # Replace with actual URL source
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('http'):
                    urls.append(href)

            self.logger.info(f"Collected {len(urls)} URLs.")
            return urls
        except Exception as e:
            self.logger.error(f"Error during data collection: {e}")
            raise

    def receive_message(self, sender, message):
        """
        Handles incoming messages from other agents.
        """
        self.logger.info(f"Received message from {sender}: {message}")

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Data Collection Agent.")
