# agents/classification_agent.py

import threading
from utils.logger import get_logger
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import logging  # Add this line

class ClassificationAgent(threading.Thread):
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.name = "ClassificationAgent"
        self.active = True
        self.logger = get_logger(self.name)
        self.model = GradientBoostingClassifier()
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)

    def run(self):
        """
        Processes incoming features for classification.
        """
        while self.active:
            time.sleep(1)  # Wait for messages to arrive

    def receive_message(self, sender, message):
        """
        Handles incoming messages from other agents.
        """
        if "features" in message:
            features = message["features"]
            classifications = self.classify(features)
            self.hub.send_message(self.name, "ResponseAgent", {"classifications": classifications})

    def classify(self, features):
        """
        Classifies URLs based on extracted features.
        """
        logger.info("Starting classification...")
        try:
            predictions = self.model.predict(features)
            logger.info(f"Classification completed. Predictions: {predictions}")
            return predictions
        except Exception as e:
            logger.error(f"Error during classification: {e}")
            raise
        features = np.array(features)
        predictions = self.model.predict(features)
        self.logger.info(f"Classified {len(features)} URLs.")
        return predictions

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Classification Agent.")
