# BustedURL API Documentation

## Overview

This document provides details about the REST APIs used in BustedURL for external communication, monitoring, and control of the system. The APIs are built using FastAPI and are designed to be secure, efficient, and easy to use.

## Base URL
http://localhost:8000/api/v1/


## Endpoints

### 1. **/status**

- **Method**: `GET`
- **Description**: Returns the current status of all agents in the system.
- **Response**:
  ```json
  {
    "data_collection_agent": "active",
    "feature_extraction_agent": "active",
    "classification_agent": "active",
    "response_agent": "inactive",
    "system_optimizer_agent": "active",
    "security_auditor_agent": "active",
    "health_monitoring_agent": "active"
  }

2. /collect
Method: POST
Description: Manually triggers the Data Collection Agent to collect new URLs.
Request Body:
json:
{
  "source": "web_traffic",
  "duration": "5min"
}

Response:
{
  "message": "Data collection started",
  "status": "success"
}

3. /classify
Method: POST
Description: Classifies a given URL as malicious or benign.
Request Body:
json:
{
  "url": "http://example.com/malicious"
}

Response:
{
  "url": "http://example.com/malicious",
  "classification": "malicious",
  "confidence": 0.95
}

4. /optimize
Method: POST
Description: Triggers the System Optimizer Agent to perform system optimization.
Response:
json:
{
  "message": "Optimization started",
  "status": "success"
}

Error Handling
All API responses will include a standard error format:
{
  "error": {
    "code": 400,
    "message": "Invalid input data"
  }
}

These APIs provide essential control and monitoring functions for the BustedURL system, allowing external integration and real-time system management.

---

### 5. **diagrams/**

- **`architecture_diagram.png`**: A visual representation of the overall architecture of the BustedURL system, including all agents and the decentralized coordination hub.
- **`state_diagram.png`**: A state diagram illustrating the states of each agent and transitions between them based on events or conditions.
- **`flow_diagram.png`**: A flow diagram showing the data and process flow between different components (agents and the coordination hub) within the system.
