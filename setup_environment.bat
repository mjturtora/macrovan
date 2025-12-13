@echo off
REM Script to set up the Poetry environment for Macrovan on Windows

REM Check if Poetry is installed
where poetry >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Poetry is not installed. Installing Poetry...
    powershell -Command "(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -"
    echo Poetry installed successfully!
) else (
    echo Poetry is already installed.
)

REM Install dependencies
echo Installing dependencies with Poetry...
poetry install

REM Create secrets.py from template if it doesn't exist
if not exist "app\secrets.py" (
    echo Creating secrets.py from template...
    copy app\secrets_template.py app\secrets.py
    echo Please edit app\secrets.py to add your VAN credentials.
) else (
    echo app\secrets.py already exists.
)

REM Run the installation tests
echo Running installation tests...
poetry run test-install
poetry run test-poetry

echo.
echo Setup complete! You can now run the VoterData automation with:
echo poetry run macrovan
echo.
echo Or activate the virtual environment with:
echo poetry shell