class ResponseAgent:
    def __init__(self, name):
        self.name = name
        self.coordination_hub = None

    def set_coordination_hub(self, hub):
        self.coordination_hub = hub

    def execute_response(self, classifications):
        """Execute actions based on classification results."""
        print(f"{self.name}: Responding to classification results...")
        for result in classifications:
            if result["label"] == "malicious":
                print(f"Blocked URL: {result['url']}")
            else:
                print(f"URL safe: {result['url']}")
        # Feedback can be sent to other agents if needed
