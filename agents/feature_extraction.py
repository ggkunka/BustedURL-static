class FeatureExtractionAgent:
    def __init__(self, name):
        self.name = name
        self.coordination_hub = None
    
    def set_coordination_hub(self, hub):
        self.coordination_hub = hub

    def extract_features(self, urls):
        """Extract features from collected URLs."""
        print(f"{self.name}: Extracting features from URLs...")
        features = [{"url": url, "feature": "example_feature"} for url in urls]  # Dummy feature extraction
        self.coordination_hub.distribute_tasks({'classification': features})
