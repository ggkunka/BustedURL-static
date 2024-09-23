from multiprocessing import Process, Queue
import time  # Ensure time is imported for sleep
from utils.logger import get_logger
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
import logging

# Configure global logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ClassificationAgent(Process):  # Inherit from Process for multiprocessing
    def __init__(self, input_queue: Queue, output_queue: Queue):
        super().__init__()
        self.input_queue = input_queue  # Queue for receiving messages
        self.output_queue = output_queue  # Queue for sending messages
        self.name = "ClassificationAgent"
        self.active = True
        self.logger = get_logger(self.name)
        self.model = GradientBoostingClassifier()
        self.is_trained = False  # Flag to check if the model is trained

    def run(self):
        """
        Processes incoming features for classification.
        """
        self.logger.info("Classification Agent started.")
        while self.active:
            try:
                if not self.input_queue.empty():
                    message = self.input_queue.get()
                    sender, data = message['sender'], message['data']
                    self.receive_message(sender, data)
                time.sleep(1)  # Wait for messages to arrive
            except Exception as e:
                self.logger.error(f"Error in {self.name}: {e}")

    def receive_message(self, sender, message):
        """
        Handles incoming messages from other agents.
        """
        if "features" in message and "labels" in message:
            features = message["features"]
            labels = message["labels"]
            classifications = self.classify(features, labels)
            self.output_queue.put({"sender": self.name, "classifications": classifications})
        elif "features" in message:
            features = message["features"]
            classifications = self.classify(features)
            self.output_queue.put({"sender": self.name, "classifications": classifications})

    def classify(self, features, true_labels=None):
        """
        Classifies URLs based on extracted features.
        If true_labels are provided, it calculates and logs the evaluation metrics.
        """
        self.logger.info("Starting classification...")
        try:
            features = np.array(features)
            
            if not self.is_trained:
                self.logger.warning("Model is not trained yet. Returning default predictions.")
                # Return default predictions or handle accordingly
                return ["benign" for _ in features]

            predictions = self.model.predict(features)
            self.logger.info(f"Classification completed. Predictions: {predictions}")

            if true_labels is not None:
                self.evaluate(predictions, true_labels)

            return predictions
        except Exception as e:
            self.logger.error(f"Error during classification: {e}")
            raise

    def train_model(self, X_train, y_train):
        """
        Train the classification model.
        """
        self.logger.info("Training classification model...")
        try:
            self.model.fit(X_train, y_train)
            self.is_trained = True
            self.logger.info("Model training completed.")
        except Exception as e:
            self.logger.error(f"Error during model training: {e}")
            raise

    def evaluate(self, predictions, true_labels):
        """
        Evaluate the performance of the classification model.
        Calculates Accuracy, Precision, Recall, F1 Score, and Confusion Matrix.
        """
        self.logger.info("Evaluating model performance...")
        try:
            accuracy = accuracy_score(true_labels, predictions)
            precision = precision_score(true_labels, predictions, pos_label='malicious', zero_division=0)
            recall = recall_score(true_labels, predictions, pos_label='malicious', zero_division=0)
            f1 = f1_score(true_labels, predictions, pos_label='malicious', zero_division=0)
            conf_matrix = confusion_matrix(true_labels, predictions, labels=['malicious', 'benign'])

            TN, FP, FN, TP = conf_matrix.ravel()

            self.logger.info(f"Accuracy: {accuracy:.4f}")
            self.logger.info(f"Precision: {precision:.4f}")
            self.logger.info(f"Recall: {recall:.4f}")
            self.logger.info(f"F1 Score: {f1:.4f}")
            self.logger.info(f"Confusion Matrix:\n{conf_matrix}")
            self.logger.info(f"True Positives (TP): {TP}")
            self.logger.info(f"True Negatives (TN): {TN}")
            self.logger.info(f"False Positives (FP): {FP}")
            self.logger.info(f"False Negatives (FN): {FN}")

            # Optionally, you can store these metrics or send them to a monitoring system
        except Exception as e:
            self.logger.error(f"Error during evaluation: {e}")
            raise

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Classification Agent.")
