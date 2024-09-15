# agents/feature_extraction_agent.py

import logging
import threading
from utils.logger import get_logger
from transformers import pipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FeatureExtractionAgent(threading.Thread):
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.name = "FeatureExtractionAgent"
        self.active = True
        self.logger = get_logger(self.name)
        self.model = pipeline("feature-extraction", model="bert-base-uncased")

    def run(self):
        """
        Processes incoming URLs for feature extraction.
        """
        while self.active:
            time.sleep(1)  # Wait for messages to arrive

    def receive_message(self, sender, message):
        """
        Handles incoming messages from other agents.
        """
        if "urls" in message:
            urls = message["urls"]
            features = self.extract_features(urls)
            self.hub.send_message(self.name, "ClassificationAgent", {"features": features})

'''
    def extract_features(self, urls):
        """
        Extracts features from URLs using a BERT model.
        """
        try:
#            logger.info(f"Extracting features for URL: {url}")
            features = self.model(url)  # Example: using a model to extract features
            logger.info(f"Feature extraction completed for URL: {url}")
            return features
        except Exception as e:
            logger.error(f"Error during feature extraction: {e}")
            raise
        features = [self.model(url) for url in urls]
        self.logger.info(f"Extracted features for {len(urls)} URLs.")
        return features
'''
    def extract_features(self, urls):
        """
        Extracts features from URLs using a BERT model.
        """
        try:
            # Initialize a list to store extracted features
            features = []
    
            # Loop through each URL and extract features
            for url in urls:
                logger.info(f"Extracting features for URL: {url}")
                url_features = self.model(url)  # Example: using a model to extract features
                features.append(url_features)
                logger.info(f"Feature extraction completed for URL: {url}")
    
            logger.info(f"Extracted features for {len(urls)} URLs.")
            return features
    
        except Exception as e:
            logger.error(f"Error during feature extraction: {e}")
            raise

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Feature Extraction Agent.")
