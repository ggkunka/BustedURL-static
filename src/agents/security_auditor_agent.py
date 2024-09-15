# agents/security_auditor_agent.py

import threading
import time
from utils.logger import get_logger
from pymongo import MongoClient

class SecurityAuditorAgent(threading.Thread):
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.name = "SecurityAuditorAgent"
        self.active = True
        self.logger = get_logger(self.name)
        self.client = MongoClient('localhost', 27017)  # Connect to MongoDB
        self.db = self.client.bustedurl_db
        self.vulnerability_collection = self.db.vulnerabilities

    def run(self):
        """
        Continuously audits the system for vulnerabilities.
        """
        while self.active:
            try:
                self.audit_security()
                time.sleep(120)  # Audit every 2 minutes
            except Exception as e:
                self.logger.error(f"Error in {self.name}: {e}")

    def audit_security(self):
        """
        Conducts a security audit and stores results in MongoDB.
        """
        vulnerabilities = self.detect_vulnerabilities()
        self.store_results(vulnerabilities)

    def detect_vulnerabilities(self):
        """
        Detects vulnerabilities by simulating security checks.
        """
        # Placeholder for real security check logic (e.g., using OWASP tools)
        vulnerabilities = [{"id": 1, "description": "SQL Injection", "severity": "High"}]
        self.logger.info(f"Detected {len(vulnerabilities)} vulnerabilities.")
        return vulnerabilities

    def store_results(self, vulnerabilities):
        """
        Stores the detected vulnerabilities in MongoDB.
        """
        for vulnerability in vulnerabilities:
            self.vulnerability_collection.insert_one(vulnerability)
            self.logger.info(f"Stored vulnerability: {vulnerability['description']}")

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Security Auditor Agent.")
