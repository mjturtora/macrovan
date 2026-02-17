@echo off
REM Script to set up the Poetry environment for Macrovan on Windows

REM Check if Poetry is installed
where poetry >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Poetry is not installed. Installing Poetry...
    
    REM Set Poetry home environment variable to C:\poetry
    set POETRY_HOME=C:\poetry
    
    REM Create the directory if it doesn't exist
    if not exist %POETRY_HOME% mkdir %POETRY_HOME%
    
    REM Install Poetry
    powershell -Command "$env:POETRY_HOME = 'C:\poetry'; (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -"
    
    REM Add Poetry to PATH
    powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';C:\poetry\bin', 'Machine')"
    
    REM Configure Poetry virtual environment location
    echo Configuring Poetry virtual environment location...
    if not exist "D:\venvs\poetry" mkdir "D:\venvs\poetry"
    C:\poetry\bin\poetry config virtualenvs.path "D:\venvs\poetry"
    
    echo Poetry installed successfully!
) else (
    echo Poetry is already installed.
)

REM Install dependencies
echo Installing dependencies with Poetry...
poetry install

REM Credentials setup
echo Configuration: Secure keyring storage enabled.
echo Note: You will be prompted for your VAN credentials on the first run.

REM Run the installation tests
echo Running installation tests...
poetry run python app/test_installation.py
poetry run python test_poetry_setup.py

echo.
echo Setup complete!
echo.
echo To run the VoterData automation:
echo poetry run vat
echo.
echo To reset or change credentials:
echo poetry run vat --reset
echo.