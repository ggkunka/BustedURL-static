# agents/data_collection_agent.py

import threading
import time
from utils.logger import get_logger
import requests

class DataCollectionAgent(threading.Thread):
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.name = "DataCollectionAgent"
        self.active = True
        self.logger = get_logger(self.name)

    def run(self):
        """
        Continuously collects URLs from various sources.
        """
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
        Simulates collecting URLs from web traffic and other sources.
        """
        # Example: Simulate URL collection using a simple request
        response = requests.get("https://example.com/urls")  # Replace with actual source
        urls = response.json().get("urls", [])
        self.logger.info(f"Collected {len(urls)} URLs.")
        return urls

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
