class DataCollectionAgent:
    def __init__(self, name):
        self.name = name
        self.coordination_hub = None
    
    def set_coordination_hub(self, hub):
        self.coordination_hub = hub

    def collect_urls(self, data_source):
        """Collect URLs from specified data sources."""
        print(f"{self.name}: Collecting URLs from {data_source}...")
        # Logic for data collection (e.g., web scraping, API integration)
        collected_data = ["http://example.com", "http://malicious.com"]  # Sample collected data
        self.coordination_hub.distribute_tasks({'feature_extraction': collected_data})
