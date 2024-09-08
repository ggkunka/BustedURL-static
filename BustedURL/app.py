from core.coordination_hub import CoordinationHub
from agents.data_collection import DataCollectionAgent
from agents.feature_extraction import FeatureExtractionAgent
from agents.classification import ClassificationAgent
from agents.response import ResponseAgent
from agents.system_optimizer import SystemOptimizerAgent
from agents.security_auditor import SecurityAuditorAgent
from agents.health_monitoring import HealthMonitoringAgent

if __name__ == "__main__":
    # Initialize the coordination hub
    hub = CoordinationHub()
    
    # Initialize agents
    data_collection_agent = DataCollectionAgent("DataCollectionAgent")
    feature_extraction_agent = FeatureExtractionAgent("FeatureExtractionAgent")
    classification_agent = ClassificationAgent("ClassificationAgent")
    response_agent = ResponseAgent("ResponseAgent")
    system_optimizer_agent = SystemOptimizerAgent("SystemOptimizerAgent")
    security_auditor_agent = SecurityAuditorAgent("SecurityAuditorAgent")
    health_monitoring_agent = HealthMonitoringAgent("HealthMonitoringAgent")

    # Register agents with the coordination hub
    hub.register_agent(data_collection_agent)
    hub.register_agent(feature_extraction_agent)
    hub.register_agent(classification_agent)
    hub.register_agent(response_agent)
    hub.register_agent(system_optimizer_agent)
    hub.register_agent(security_auditor_agent)
    hub.register_agent(health_monitoring_agent)

    # Start the workflow
    hub.distribute_tasks({'collect_data': 'example_source'})
