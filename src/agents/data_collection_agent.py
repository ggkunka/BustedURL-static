# agents/data_collection_agent.py

import threading
import time
import requests
from bs4 import BeautifulSoup
from utils.logger import get_logger

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
        Collects URLs from web sources using BeautifulSoup.
        """
        urls = []
        response = requests.get("https://example.com/urls")  # Replace with actual source
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a'):
            urls.append(link.get('href'))
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
