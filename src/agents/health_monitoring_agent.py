# agents/health_monitoring_agent.py

import psutil
import threading
import time
from prometheus_client import Gauge
from utils.logger import get_logger

class HealthMonitoringAgent(threading.Thread):
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.name = "HealthMonitoringAgent"
        self.active = True
        self.logger = get_logger(self.name)

        # Prometheus Gauges to monitor system health
        self.cpu_gauge = Gauge('system_cpu_usage', 'CPU usage of the system')
        self.memory_gauge = Gauge('system_memory_usage', 'Memory usage of the system')
        self.disk_gauge = Gauge('system_disk_usage', 'Disk usage of the system')

    def run(self):
        """
        Continuously monitors system health.
        """
        self.logger.info("Health Monitoring Agent started.")
        while self.active:
            self.monitor_health()
            time.sleep(5)  # Monitor every 5 seconds

    def monitor_health(self):
        """
        Monitors system CPU, memory, and disk usage.
        """
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        # Update Prometheus Gauges
        self.cpu_gauge.set(cpu_usage)
        self.memory_gauge.set(memory_usage)
        self.disk_gauge.set(disk_usage)

        self.logger.info(f"CPU: {cpu_usage}%, Memory: {memory_usage}%, Disk: {disk_usage}%")

        # Alert if resource usage exceeds a threshold
        if cpu_usage > 85:
            self.logger.warning(f"High CPU usage detected: {cpu_usage}%")
        if memory_usage > 85:
            self.logger.warning(f"High Memory usage detected: {memory_usage}%")
        if disk_usage > 85:
            self.logger.warning(f"High Disk usage detected: {disk_usage}%")

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Health Monitoring Agent.")
