# agents/response_agent.py

import threading
import time
from utils.logger import get_logger
from cryptography.fernet import Fernet

class ResponseAgent(threading.Thread):
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.name = "ResponseAgent"
        self.active = True
        self.logger = get_logger(self.name)
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)

    def run(self):
        """
        Listens for messages from other agents and takes action based on classification.
        """
        while self.active:
            time.sleep(1)  # Wait for messages to arrive

    def receive_message(self, sender, message):
        """
        Handles incoming messages from other agents.
        """
        if "classifications" in message:
            classifications = message["classifications"]
            self.take_action(classifications)

    def take_action(self, classifications):
        """
        Takes action based on URL classification results.
        Encrypts and logs the results, sends alerts or blocks URLs.
        """
        for url, classification in classifications.items():
            encrypted_url = self.cipher.encrypt(url.encode())
            if classification == "malicious":
                self.logger.warning(f"Blocked URL: {url}")
                # Example: Implement an API call or firewall rule to block the URL
                self.send_alert(url, encrypted_url)
            else:
                self.logger.info(f"URL is benign: {url}")

    def send_alert(self, url, encrypted_url):
        """
        Sends an alert for a malicious URL.
        """
        # Placeholder for alert logic (e.g., send email or SMS alert)
        self.logger.info(f"Alert sent for malicious URL: {url}, Encrypted: {encrypted_url}")

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Response Agent.")
