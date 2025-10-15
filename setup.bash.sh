#!/bin/bash

# Project name
PROJECT_NAME="TeleLang"

# Check that we are in the correct folder
if [ "$(basename "$PWD")" != "$PROJECT_NAME" ]; then
    echo "Error: you need to run the script from the $PROJECT_NAME folder"
    exit 1
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found, installing..."
    
    # For Ubuntu/Debian
    if [ -f /etc/debian_version ]; then
        sudo apt update
        sudo apt install -y python3 python3-venv python3-pip
    else
        echo "Automatic Python installation is not supported for this OS, please install manually"
        exit 1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
fi

# Activate venv
source venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "requirements.txt file not found!"
fi

# Ask whether to run main.py or exit
read -p "Run main.py? (y/n): " RUN_MAIN
if [[ "$RUN_MAIN" == "y" || "$RUN_MAIN" == "Y" ]]; then
    if [ -f "main.py" ]; then
        python main.py
    else
        echo "main.py not found!"
    fi
else
    echo "Exiting."
fi
