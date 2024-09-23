# agents/system_optimizer_agent.py

from multiprocessing import Process
import psutil
import time
from utils.logger import get_logger

class SystemOptimizerAgent(Process):  # Switch to Process for multiprocessing
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.name = "SystemOptimizerAgent"
        self.active = True
        self.logger = get_logger(self.name)

    def run(self):
        """
        Continuously monitors system performance and optimizes resources.
        """
        self.logger.info("System Optimizer Agent started.")
        while self.active:
            try:
                self.optimize_system()
                time.sleep(10)  # Adjust optimization interval
            except Exception as e:
                self.logger.error(f"Error in {self.name}: {e}")

    def optimize_system(self):
        """
        Optimizes system performance by adjusting resource usage based on CPU and memory stats.
        """
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        if cpu_usage > 80:
            self.logger.warning(f"High CPU usage detected: {cpu_usage}%. Attempting to optimize.")
            self.adjust_parameters(cpu_usage)
        elif memory_usage > 80:
            self.logger.warning(f"High Memory usage detected: {memory_usage}%. Attempting to optimize.")
            self.adjust_parameters(memory_usage)
        else:
            self.logger.info(f"System is operating normally. CPU: {cpu_usage}%, Memory: {memory_usage}%.")

    def adjust_parameters(self, usage):
        """
        Adjust system parameters based on the given usage (CPU or Memory).
        Example: Reduce number of threads or limit resource-intensive tasks.
        """
        self.logger.info(f"Adjusting parameters based on usage: {usage}%")
        # Placeholder for actual adjustment logic: Scaling down tasks, reducing workload, or tuning models.

    def stop(self):
        """
        Stops the agent's execution.
        """
        self.active = False
        self.logger.info("Stopping System Optimizer Agent.")
