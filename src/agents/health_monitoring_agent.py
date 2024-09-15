# src/agents/health_monitoring_agent.py

import threading
import logging
from prometheus_client import CollectorRegistry, Gauge
from utils.logger import get_logger
import psutil

logger = get_logger("HealthMonitoringAgent")


class HealthMonitoringAgent(threading.Thread):
    def __init__(self, coordination_hub):
        super().__init__(daemon=True)  # Initialize the Thread with daemon=True to ensure it runs in the background
        self.coordination_hub = coordination_hub

        # Create a unique registry for this agent to avoid duplicate registration errors
        self.registry = CollectorRegistry()
        self.cpu_gauge = Gauge('system_cpu_usage', 'CPU usage of the system', registry=self.registry)
        self.memory_gauge = Gauge('system_memory_usage', 'Memory usage of the system', registry=self.registry)
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)

    def run(self):
        """Override the run method to start monitoring in a separate thread."""
        # Start the monitoring threads for CPU and memory usage
        self.monitor_cpu_usage()
        self.monitor_memory_usage()

    def monitor_cpu_usage(self):
        """Monitor and update CPU usage."""
        while True:
            try:
                cpu_usage = psutil.cpu_percent(interval=1)
                self.cpu_gauge.set(cpu_usage)
                logger.info(f"CPU Usage: {cpu_usage}%")
            except Exception as e:
                logger.error(f"Error monitoring CPU usage: {e}")

    def monitor_memory_usage(self):
        """Monitor and update Memory usage."""
        while True:
            try:
                memory_usage = psutil.virtual_memory().percent
                self.memory_gauge.set(memory_usage)
                logger.info(f"Memory Usage: {memory_usage}%")
            except Exception as e:
                logger.error(f"Error monitoring memory usage: {e}")
