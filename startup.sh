#!/bin/bash

echo "Starting startup script..." > /home/site/wwwroot/startup.log

# Install LibreOffice if not installed
if ! command -v libreoffice &> /dev/null; then
    echo "Installing LibreOffice..." >> /home/site/wwwroot/startup.log
    apt-get update && apt-get install -y libreoffice
else
    echo "LibreOffice is already installed." >> /home/site/wwwroot/startup.log
fi

# Change to the application directory
cd /home/site/wwwroot

# Start FastAPI with Gunicorn
echo "Starting FastAPI application..." >> /home/site/wwwroot/startup.log
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app >> /home/site/wwwroot/startup.log 2>&1
