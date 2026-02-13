#!/bin/bash
# Script to set up the Poetry environment for Macrovan

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    
    # Set Poetry home environment variable
    export POETRY_HOME="/usr/local/poetry"
    
    # Create the directory if it doesn't exist
    if [ ! -d "$POETRY_HOME" ]; then
        sudo mkdir -p "$POETRY_HOME"
    fi
    
    # Install Poetry
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Configure Poetry virtual environment location
    echo "Configuring Poetry virtual environment location..."
    mkdir -p "$HOME/venvs/poetry"
    poetry config virtualenvs.path "$HOME/venvs/poetry"
    
    echo "Poetry installed successfully!"
else
    echo "Poetry is already installed."
fi

# Install dependencies
echo "Installing dependencies with Poetry..."
poetry install

# Credentials setup
echo "Configuration: Secure keyring storage enabled."
echo "Note: You will be prompted for your VAN credentials on the first run."

# Run the installation tests
echo "Running installation tests..."
poetry run python app/test_installation.py
poetry run python test_poetry_setup.py

echo ""
echo "Setup complete!"
echo ""
echo "To run the VoterData automation:"
echo "poetry run vat"
echo ""
echo "To reset or change credentials:"
echo "poetry run vat --reset"
echo ""