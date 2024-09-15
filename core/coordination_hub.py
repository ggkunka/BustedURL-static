class CoordinationHub:
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, agent):
        """Register an agent with the coordination hub."""
        self.agents[agent.name] = agent
        agent.set_coordination_hub(self)
    
    def distribute_tasks(self, task_data):
        """Distribute tasks to agents based on their roles."""
        if 'collect_data' in task_data:
            self.agents['DataCollectionAgent'].collect_urls(task_data['collect_data'])
        if 'feature_extraction' in task_data:
            self.agents['FeatureExtractionAgent'].extract_features(task_data['feature_extraction'])
        if 'classification' in task_data:
            self.agents['ClassificationAgent'].classify_urls(task_data['classification'])
        # Add more task distributions as needed
    
    def synchronize_agents(self):
        """Handle agent synchronization and inter-agent communication."""
        # Implement logic to facilitate communication between agents
        pass

    def optimize_system(self):
        """Optimize system performance based on feedback from agents."""
        # Implement logic for optimization based on agent feedback
        pass
