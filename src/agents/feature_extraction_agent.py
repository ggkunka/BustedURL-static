from multiprocessing import Process, Queue
import logging
import time
from transformers import pipeline
from utils.logger import get_logger
import numpy as np  # To combine feature outputs

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FeatureExtractionAgent(Process):  # Use Process for multiprocessing
    def __init__(self, input_queue: Queue, output_queue: Queue):
        super().__init__()
        self.input_queue = input_queue  # Queue to receive messages
        self.output_queue = output_queue  # Queue to send messages
        self.name = "FeatureExtractionAgent"
        self.active = True
        self.logger = get_logger(self.name)

        # Load multiple transformer models for ensemble learning
        self.models = {
            "bert": pipeline("feature-extraction", model="bert-base-uncased", clean_up_tokenization_spaces=False),
            "roberta": pipeline("feature-extraction", model="roberta-base", clean_up_tokenization_spaces=False),
            "xlnet": pipeline("feature-extraction", model="xlnet-base-cased", clean_up_tokenization_spaces=False),
            "distilbert": pipeline("feature-extraction", model="distilbert-base-uncased", clean_up_tokenization_spaces=False)
        }

    def run(self):
        """
        Continuously processes incoming URLs for feature extraction.
        """
        self.logger.info(f"{self.name} started.")
        while self.active:
            try:
                if not self.input_queue.empty():
                    message = self.input_queue.get()
                    sender, data = message['sender'], message['data']
                    self.receive_message(sender, data)
                time.sleep(1)  # Adjust the frequency as needed
            except Exception as e:
                self.logger.error(f"Error in {self.name}: {e}")

    def receive_message(self, sender, message):
        """
        Handles incoming messages from other agents.
        """
        if "urls" in message:
            urls = message["urls"]
            features = self.extract_features(urls)
            self.output_queue.put({"sender": self.name, "features": features})

    def extract_features(self, urls):
        """
        Extracts features from URLs using an ensemble of transformer models (BERT, RoBERTa, XLNet, DistilBERT).
        """
        try:
            features = []

            # Extract features for each URL
            for url in urls:
                self.logger.info(f"Extracting features for URL: {url}")

                # Run each model and collect features
                url_features = {model_name: self.models[model_name](url) for model_name in self.models}
                
                # Combine features from all models using an ensemble method
                combined_features = self.combine_features(url_features)
                
                features.append(combined_features)
                self.logger.info(f"Feature extraction completed for URL: {url}")

            self.logger.info(f"Extracted features for {len(urls)} URLs.")
            return features

        except Exception as e:
            self.logger.error(f"Error during feature extraction: {e}")
            return []

    def combine_features(self, url_features):
        """
        Combines features from multiple transformer models into a single feature vector.
        You can use averaging, concatenation, or other ensemble methods.
        """
        try:
            # Here we use simple averaging of the feature vectors from all models
            model_feature_vectors = [np.array(features[0]) for features in url_features.values()]  # Extract the feature arrays
            combined_features = np.mean(model_feature_vectors, axis=0)  # Take the average of all model outputs
            return combined_features.tolist()

        except Exception as e:
            self.logger.error(f"Error during feature combination: {e}")
            return []

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Feature Extraction Agent.")
