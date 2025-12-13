#!/bin/bash
# Script to set up the Poetry environment for Macrovan

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo "Poetry installed successfully!"
else
    echo "Poetry is already installed."
fi

# Install dependencies
echo "Installing dependencies with Poetry..."
poetry install

# Create secrets.py from template if it doesn't exist
if [ ! -f "app/secrets.py" ]; then
    echo "Creating secrets.py from template..."
    cp app/secrets_template.py app/secrets.py
    echo "Please edit app/secrets.py to add your VAN credentials."
else
    echo "app/secrets.py already exists."
fi

# Run the installation tests
echo "Running installation tests..."
poetry run test-install
poetry run test-poetry

echo ""
echo "Setup complete! You can now run the VoterData automation with:"
echo "poetry run macrovan"
echo ""
echo "Or activate the virtual environment with:"
echo "poetry shell"