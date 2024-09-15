# scripts/deploy.ps1

# Set Environment Variables
$env:PYTHONPATH = "C:\Python39"
$env:VIRTUAL_ENV = "C:\bustedurl\venv"

# Install Dependencies
Write-Output "Installing dependencies..."
python -m venv bustedurl
bustedurl\Scripts\Activate.ps1
pip install -r requirements.txt

# Start Services (MongoDB, RabbitMQ, etc.)
Write-Output "Starting MongoDB service..."
Start-Service -Name MongoDB

Write-Output "Starting RabbitMQ service..."
Start-Service -Name RabbitMQ

# Deploy BustedURL Components
Write-Output "Deploying BustedURL agents..."
Start-Process -FilePath "python.exe" -ArgumentList "agents\data_collection_agent.py" -NoNewWindow
Start-Process -FilePath "python.exe" -ArgumentList "agents\feature_extraction_agent.py" -NoNewWindow
Start-Process -FilePath "python.exe" -ArgumentList "agents\classification_agent.py" -NoNewWindow
# Repeat for all other agents...

Write-Output "Deployment completed."
