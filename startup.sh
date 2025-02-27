#!/bin/bash

# Define source and destination directories
SOURCE_DIR="/tmp/8dd56f4b614798f"
DEST_DIR="/home/app"

# Ensure destination directory exists
mkdir -p $DEST_DIR

# Move all files to /home/app
cp -r $SOURCE_DIR/* $DEST_DIR/

# Ensure proper ownership and permissions
sudo chown -R $(whoami):$(whoami) $DEST_DIR
chmod -R 755 $DEST_DIR

# Install LibreOffice if not installed
if ! command -v libreoffice &> /dev/null
then
    echo "LibreOffice not found, installing..."
    sudo apt-get update && sudo apt-get install -y libreoffice
fi

# Activate virtual environment
source $DEST_DIR/antenv/bin/activate

# Change to the new app directory
cd $DEST_DIR

# Start FastAPI app with Gunicorn
exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
