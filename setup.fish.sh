#!/usr/bin/env fish

# Project name
set PROJECT_NAME "TeleLang"

# Check that we are in the correct folder
if test (basename $PWD) != $PROJECT_NAME
    echo "Error: you need to run the script from the $PROJECT_NAME folder"
    exit 1
end

# Check for Python 3
if not type -q python3
    echo "Python3 not found, installing..."
    
    # For Ubuntu/Debian
    if test -f /etc/debian_version
        sudo apt update
        sudo apt install -y python3 python3-venv python3-pip
    else
        echo "Automatic Python installation is not supported for this OS, please install manually"
        exit 1
    end
end

# Create virtual environment if it doesn't exist
if not test -d "venv"
    python3 -m venv venv
    echo "Virtual environment created"
end

# Activate venv
. venv/bin/activate.fish

# Install dependencies
if test -f "requirements.txt"
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "requirements.txt file not found!"
end

# Ask whether to run main.py or exit
read -P "Run main.py? (y/n): " RUN_MAIN
if test $RUN_MAIN = "y" -o $RUN_MAIN = "Y"
    if test -f "main.py"
        python main.py
    else
        echo "main.py not found!"
    end
else
    echo "Exiting."
end
