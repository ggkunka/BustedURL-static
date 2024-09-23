from multiprocessing import Process, Queue
import psutil
import time
from prometheus_client import Gauge
from utils.logger import get_logger

# Prometheus Gauges - Defined globally to avoid duplicate timeseries
cpu_gauge = Gauge('system_cpu_usage', 'CPU usage of the system')
memory_gauge = Gauge('system_memory_usage', 'Memory usage of the system')
disk_gauge = Gauge('system_disk_usage', 'Disk usage of the system')

class HealthMonitoringAgent(Process):  # Still using Process for multiprocessing
    def __init__(self, input_queue: Queue, output_queue: Queue):  # Using queues instead of hub
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.name = "HealthMonitoringAgent"
        self.active = True
        self.logger = get_logger(self.name)

    def run(self):
        """
        Continuously monitors system health.
        """
        self.logger.info("Health Monitoring Agent started.")
        while self.active:
            try:
                self.monitor_health()
                time.sleep(5)  # Monitor every 5 seconds
            except Exception as e:
                self.logger.error(f"Error in {self.name}: {e}")

    def monitor_health(self):
        """
        Monitors system CPU, memory, and disk usage.
        """
        try:
            # Collect system metrics
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent

            # DEBUG: Log raw metric values before formatting
            self.logger.debug(f"Raw CPU usage: {cpu_usage}, Memory usage: {memory_usage}, Disk usage: {disk_usage}")

            # Check if the metrics are valid and log them
            if isinstance(cpu_usage, (int, float)) and isinstance(memory_usage, (int, float)) and isinstance(disk_usage, (int, float)):
                self.logger.debug(f"Valid metrics - CPU: {cpu_usage}, Memory: {memory_usage}, Disk: {disk_usage}")

                # Update global Prometheus Gauges
                cpu_gauge.set(float(cpu_usage))
                memory_gauge.set(float(memory_usage))
                disk_gauge.set(float(disk_usage))

                # Properly format and log system health
                self.logger.info(f"System Health - CPU: {cpu_usage:.2f}%, Memory: {memory_usage:.2f}%, Disk: {disk_usage:.2f}%")
            else:
                self.logger.warning(f"Invalid data types detected - CPU: {cpu_usage}, Memory: {memory_usage}, Disk: {disk_usage}")

            # Alert if resource usage exceeds a threshold
            if cpu_usage > 85.0:
                self.logger.warning(f"High CPU usage detected: {cpu_usage:.2f}%")
            if memory_usage > 85.0:
                self.logger.warning(f"High Memory usage detected: {memory_usage:.2f}%")
            if disk_usage > 85.0:
                self.logger.warning(f"High Disk usage detected: {disk_usage:.2f}%")

        except Exception as e:
            # DEBUG: Log exact exception details
            self.logger.error(f"Error while monitoring system health: {e}", exc_info=True)

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Health Monitoring Agent.")
