from multiprocessing import Process, Queue
import psutil
import time
from prometheus_client import Gauge
from utils.logger import get_logger

# Prometheus Gauges - Defined globally to avoid duplicate timeseries
cpu_gauge = Gauge('system_cpu_usage', 'CPU usage of the system')
memory_gauge = Gauge('system_memory_usage', 'Memory usage of the system')
disk_gauge = Gauge('home_disk_usage', 'Disk usage of the /home/yzhang10 partition')

class HealthMonitoringAgent(Process):
    def __init__(self, input_queue: Queue, output_queue: Queue):
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
        Monitors system CPU, memory, and disk usage for the /home/yzhang10 partition.
        """
        try:
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent

            # Monitor /home/yzhang10 partition
            partitions = psutil.disk_partitions()
            disk_usage = -1  # Default value if the partition is not found
            for partition in partitions:
                if partition.mountpoint == '/home/yzhang10':  # Monitor /home/yzhang10
                    try:
                        disk_usage = psutil.disk_usage(partition.mountpoint).percent
                    except Exception as e:
                        self.logger.warning(f"Error reading {partition.mountpoint} partition: {e}")

            if disk_usage == -1:
                self.logger.warning(f"Unable to retrieve disk usage from /home/yzhang10.")

            # Update Prometheus Gauges
            cpu_gauge.set(cpu_usage)
            memory_gauge.set(memory_usage)
            if disk_usage != -1:
                disk_gauge.set(disk_usage)

            self.logger.info(f"CPU: {cpu_usage}%, Memory: {memory_usage}%, Disk: {disk_usage}%")

            # Alert if resource usage exceeds a threshold
            if cpu_usage > 85:
                self.logger.warning(f"High CPU usage detected: {cpu_usage}%")
            if memory_usage > 85:
                self.logger.warning(f"High Memory usage detected: {memory_usage}%")
            if disk_usage > 85:
                self.logger.warning(f"High Disk usage detected: {disk_usage}%")

        except Exception as e:
            self.logger.error(f"Error while monitoring system health: {e}")

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping Health Monitoring Agent.")
