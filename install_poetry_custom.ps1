# PowerShell script to install Poetry to C:\poetry

Write-Host "Starting Poetry installation..." -ForegroundColor Cyan

# 1. Install Poetry to C:\poetry
try {
    Write-Host "Installing Poetry to C:\poetry..." -ForegroundColor Yellow
    
    # Set Poetry home environment variable
    $env:POETRY_HOME = "C:\poetry"
    
    # Create the directory if it doesn't exist
    if (-not (Test-Path $env:POETRY_HOME)) {
        New-Item -Path $env:POETRY_HOME -ItemType Directory -Force | Out-Null
        Write-Host "Created Poetry home directory." -ForegroundColor Green
    }
    
    # Install Poetry
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    
    Write-Host "Poetry installed successfully." -ForegroundColor Green
} catch {
    Write-Host "Error installing Poetry: $_" -ForegroundColor Red
    exit 1
}

# 2. Add Poetry to the system PATH
try {
    Write-Host "Adding Poetry to system PATH..." -ForegroundColor Yellow
    
    # Get current machine PATH
    $machinePath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)
    
    # Check if Poetry path is already in PATH
    if ($machinePath -notlike "*C:\poetry\bin*") {
        # Add Poetry to PATH
        [Environment]::SetEnvironmentVariable("Path", $machinePath + ";C:\poetry\bin", [EnvironmentVariableTarget]::Machine)
        Write-Host "Added Poetry to system PATH." -ForegroundColor Green
    } else {
        Write-Host "Poetry is already in system PATH." -ForegroundColor Green
    }
    
    # Refresh environment variables in current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
} catch {
    Write-Host "Error adding Poetry to PATH: $_" -ForegroundColor Red
    exit 1
}

# 3. Configure Poetry virtual environment location
try {
    Write-Host "Configuring Poetry virtual environment location..." -ForegroundColor Yellow
    
    # Create directory for virtual environments if it doesn't exist
    if (-not (Test-Path "D:\venvs\poetry")) {
        New-Item -Path "D:\venvs\poetry" -ItemType Directory -Force | Out-Null
        Write-Host "Created virtual environments directory." -ForegroundColor Green
    }
    
    # Set virtual environments path
    & "C:\poetry\bin\poetry" config virtualenvs.path "D:\venvs\poetry"
    
    Write-Host "Configured Poetry virtual environment location." -ForegroundColor Green
} catch {
    Write-Host "Error configuring virtual environment location: $_" -ForegroundColor Red
    exit 1
}

# 4. Verify Poetry installation
try {
    Write-Host "Verifying Poetry installation..." -ForegroundColor Yellow
    
    # Check Poetry version
    $poetryVersion = & "C:\poetry\bin\poetry" --version
    Write-Host "Poetry version: $poetryVersion" -ForegroundColor Green
    
    # Check Poetry configuration
    Write-Host "Poetry configuration:" -ForegroundColor Yellow
    & "C:\poetry\bin\poetry" config --list
} catch {
    Write-Host "Error verifying Poetry installation: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Poetry installation and configuration completed successfully." -ForegroundColor Cyan
Write-Host "You may need to restart your terminal or IDE for the PATH changes to take effect." -ForegroundColor Yellow