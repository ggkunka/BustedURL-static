# agents/system_optimizer_agent.py

import threading
import time
import psutil
from utils.logger import get_logger

class SystemOptimizerAgent(threading.Thread):
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.name = "SystemOptimizerAgent"
        self.active = True
        self.logger = get_logger(self.name)

    def run(self):
        """
        Continuously monitors and optimizes system performance.
        """
        while self.active:
            try:
                self.optimize_system()
                time.sleep(30)  # Optimize every 30 seconds
            except Exception as e:
                self.logger.error(f"Error in {self.name}: {e}")

    def optimize_system(self):
        """
        Optimizes system resources by monitoring CPU and memory usage.
        """
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        self.logger.info(f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_info.percent}%")
        
        if cpu_usage > 80:
            self.logger.warning("High CPU usage detected. Optimizing workload distribution...")
            # Placeholder for optimization logic (e.g., reduce workload, scale resources)

        if memory_info.percent > 75:
            self.logger.warning("High memory usage detected. Optimizing memory usage...")
            # Placeholder for optimization logic (e.g., free up memory, garbage collection)

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping System Optimizer Agent.")
