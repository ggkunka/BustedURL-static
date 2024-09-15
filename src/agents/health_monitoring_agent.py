# agents/health_monitoring_agent.py

import threading
import time
import prometheus_client
from prometheus_client import Gauge
from utils.logger import get_logger

class HealthMonitoringAgent(threading.Thread):
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.name = "HealthMonitoringAgent"
        self.active = True
        self.logger = get_logger(self.name)
        self.cpu_gauge = Gauge('system_cpu_usage', 'CPU usage of the system')
        self.memory_gauge = Gauge('system_memory_usage', 'Memory usage of the system')
        prometheus_client.start_http_server(8000)  # Start Prometheus metrics server

    def run(self):
        """
        Continuously monitors system health.
        """
        while self.active:
            try:
                self.monitor_health()
                time.sleep(15)  # Monitor every 15 seconds
            except Exception as e:
                self.logger.error(f"Error in {self.name}: {e}")

    def monitor_health(self):
        """
        Monitors system health metrics such as CPU and memory usage.
        """
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        self.cpu_gauge.set(cpu_usage)
        self.memory_gauge.set(memory_usage)
        self.logger.info(f"Monitored CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}%")

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Health Monitoring Agent.")
