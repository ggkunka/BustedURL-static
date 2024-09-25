from multiprocessing import Process, Queue
import logging
import time
import requests
import pandas as pd
import os
from bs4 import BeautifulSoup
from utils.logger import get_logger

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory paths
RAW_DATA_PATH = 'data/raw/'
PROCESSED_DATA_PATH = 'data/processed/'

# Ensure directories exist
os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

class DataCollectionAgent(Process):  # Use Process instead of Thread
    def __init__(self, input_queue: Queue, output_queue: Queue, collection_interval=86400):  # Interval set to 1 day (86400 seconds)
        super().__init__()
        self.input_queue = input_queue  # Queue for receiving messages
        self.output_queue = output_queue  # Queue for sending messages
        self.name = "DataCollectionAgent"
        self.active = True
        self.collection_interval = collection_interval  # Interval between data collections (delta updates)
        self.logger = get_logger(self.name)

    def run(self):
        """
        Continuously collects URLs from various sources and sends them to the FeatureExtractionAgent.
        """
        self.logger.info(f"{self.name} started.")
        while self.active:
            try:
                if not self.input_queue.empty():
                    message = self.input_queue.get()
                    sender, data = message['sender'], message['data']
                    self.receive_message(sender, data)

                urls = self.collect_urls()
                if urls:
                    # Save raw URLs
                    self.save_urls(urls, 'raw_urls.csv', raw=True)

                    # Here you could add any additional data cleaning if necessary
                    cleaned_urls = self.clean_urls(urls)

                    # Save processed URLs
                    self.save_urls(cleaned_urls, 'cleaned_urls.csv', raw=False)

                    self.output_queue.put({"sender": self.name, "urls": cleaned_urls})

                time.sleep(self.collection_interval)  # Collect URLs based on the specified interval
            except Exception as e:
                self.logger.error(f"Error in {self.name}: {e}")

    def collect_urls(self):
        """
        Collects URLs from multiple web sources, including OpenPhish, PhishTank, and more.
        """
        self.logger.info("Starting data collection from multiple sources...")
        urls = []

        # Collect from OpenPhish
        urls += self.collect_from_openphish()

        # Collect from PhishTank
        urls += self.collect_from_phishtank()

        # Collect from Alexa Top Sites (Benign URLs)
        urls += self.collect_from_alexa()

        # Optionally, collect from Phishing.Database (if desired)
        urls += self.collect_from_phishing_database()

        # Commenting out Google Chrome History fetching as it's a server environment
        # urls += self.collect_from_chrome_history()

        self.logger.info(f"Total URLs collected: {len(urls)}")
        return urls

    def collect_from_openphish(self):
        """
        Collects malicious URLs from OpenPhish.
        """
        self.logger.info("Collecting URLs from OpenPhish...")
        openphish_url = "https://openphish.com/feed.txt"
        urls = []
        try:
            response = requests.get(openphish_url)
            if response.status_code == 200:
                urls = response.text.splitlines()
                self.logger.info(f"Collected {len(urls)} URLs from OpenPhish.")
            else:
                self.logger.warning(f"Failed to collect from OpenPhish. Status code: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error collecting from OpenPhish: {e}")
        return urls

    def collect_from_phishtank(self):
        """
        Collects malicious URLs from PhishTank.
        """
        self.logger.info("Collecting URLs from PhishTank...")
        phishtank_url = "http://data.phishtank.com/data/online-valid.csv"
        urls = []
        try:
            response = requests.get(phishtank_url)
            if response.status_code == 200:
                df = pd.read_csv(pd.compat.StringIO(response.text))
                urls = df['url'].tolist()
                self.logger.info(f"Collected {len(urls)} URLs from PhishTank.")
            else:
                self.logger.warning(f"Failed to collect from PhishTank. Status code: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error collecting from PhishTank: {e}")
        return urls

    def collect_from_alexa(self):
        """
        Collects benign URLs from Alexa's top sites.
        """
        self.logger.info("Collecting benign URLs from Alexa Top Sites...")
        alexa_url = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
        urls = []
        try:
            response = requests.get(alexa_url)
            if response.status_code == 200:
                df = pd.read_csv(pd.compat.StringIO(response.text), header=None, names=['rank', 'url'])
                urls = df['url'].tolist()
                self.logger.info(f"Collected {len(urls)} benign URLs from Alexa Top Sites.")
            else:
                self.logger.warning(f"Failed to collect from Alexa Top Sites. Status code: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error collecting from Alexa Top Sites: {e}")
        return urls

    def collect_from_phishing_database(self):
        """
        Collects malicious URLs from Phishing.Database.
        """
        self.logger.info("Collecting URLs from Phishing.Database...")
        phishing_db_url = "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ALL.txt"
        urls = []
        try:
            response = requests.get(phishing_db_url)
            if response.status_code == 200:
                urls = response.text.splitlines()
                self.logger.info(f"Collected {len(urls)} URLs from Phishing.Database.")
            else:
                self.logger.warning(f"Failed to collect from Phishing.Database. Status code: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error collecting from Phishing.Database: {e}")
        return urls

    def clean_urls(self, urls):
        """
        Cleans the URLs by removing duplicates and ensuring well-formed URLs.
        """
        self.logger.info("Cleaning collected URLs...")
        cleaned_urls = list(set(urls))  # Removing duplicates
        self.logger.info(f"Cleaned URLs, reduced to {len(cleaned_urls)} from {len(urls)} original URLs.")
        return cleaned_urls

    def save_urls(self, urls, filename, raw=True):
        """
        Saves URLs to the appropriate directory (raw or processed).
        """
        if raw:
            path = os.path.join(RAW_DATA_PATH, filename)
        else:
            path = os.path.join(PROCESSED_DATA_PATH, filename)
        
        try:
            df = pd.DataFrame(urls, columns=['url'])
            df.to_csv(path, index=False)
            self.logger.info(f"Saved {len(urls)} URLs to {path}")
        except Exception as e:
            self.logger.error(f"Error saving URLs to {path}: {e}")

    # Commenting out Chrome History fetching as it's a server environment
    # def collect_from_chrome_history(self):
    #     """
    #     Collects benign URLs from Google Chrome browsing history (only applicable in local environments).
    #     """
    #     self.logger.info("Collecting URLs from Google Chrome History...")
    #     # Fetching Chrome history logic would go here
    #     urls = []
    #     return urls

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
