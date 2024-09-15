# core/coordination_hub.py

import threading
from utils.logger import get_logger

class CoordinationHub:
    def __init__(self):
        self.agents = {}
        self.lock = threading.Lock()
        self.logger = get_logger("CoordinationHub")

    def register_agent(self, agent):
        """
        Registers an agent with the coordination hub.
        """
        with self.lock:
            self.agents[agent.name] = agent
            self.logger.info(f"Agent {agent.name} registered.")

    def start(self):
        """
        Starts the coordination hub.
        """
        self.logger.info("Coordination Hub started.")

    def stop(self):
        """
        Stops all agents and shuts down the hub.
        """
        with self.lock:
            for agent_name, agent in self.agents.items():
                agent.stop()
                self.logger.info(f"Agent {agent_name} stopped.")
            self.logger.info("Coordination Hub stopped.")

    def send_message(self, sender, receiver, message):
        """
        Sends a message from one agent to another.
        """
        with self.lock:
            if receiver in self.agents:
                self.agents[receiver].receive_message(sender, message)
                self.logger.info(f"Message sent from {sender} to {receiver}: {message}")
            else:
                self.logger.warning(f"Failed to send message from {sender} to {receiver}: Receiver not found.")

    def monitor_agents(self):
        """
        Monitors all registered agents.
        """
        with self.lock:
            for agent_name, agent in self.agents.items():
                if not agent.is_alive():
                    self.logger.error(f"Agent {agent_name} is not responding. Restarting...")
                    agent.start()
