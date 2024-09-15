class ClassificationAgent:
    def __init__(self, name):
        self.name = name
        self.coordination_hub = None

    def set_coordination_hub(self, hub):
        self.coordination_hub = hub

    def classify_urls(self, features):
        """Classify URLs based on extracted features."""
        print(f"{self.name}: Classifying URLs...")
        # Example: A simple threshold-based classification
        classifications = [{"url": f["url"], "label": "malicious" if "malicious" in f["url"] else "benign"} for f in features]
        self.coordination_hub.distribute_tasks({'response': classifications})
