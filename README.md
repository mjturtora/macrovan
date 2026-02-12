# Macrovan

Macrovan is a Robotic Process Automation (RPA) toolkit designed to automate various tasks related to voter data management, campaign operations, and volunteer coordination.

## Overview

Macrovan provides automation for several critical campaign operations:

### VAT Automation
- Downloads VoterData files (G01-G10) from the API
- Manages files in VAN (VoteBuilder) including deletion and bulk uploads
- Processes saved searches and updates lists in the "VAT Lists (MT)" folder

### Vote-By-Mail (VBM) Targeting
- Automates the printing of VBM target lists and labels
- Processes Excel inputs to generate properly formatted outputs
- Organizes printed materials by organizer/volunteer

### PDF Processing and Organization
- Extracts information from generated PDFs
- Creates organizer-specific folders for output distribution
- Manages file cleanup and organization

## Requirements

- Python 3.7 or higher
- Dependencies listed in `pyproject.toml` (managed by Poetry)
- Chrome browser installed
- Internet connection
- VAN account with appropriate permissions (for VoterData automation)

## Installation

### Option 1: Using Poetry (Recommended)

[Poetry](https://python-poetry.org/) is a modern dependency management and packaging tool for Python. It's the recommended way to set up the environment for Macrovan.

1. Run the setup script:

   **On Windows:**
   ```
   setup_environment.bat
   ```

   **On macOS/Linux:**
   ```
   ./setup_environment.sh
   ```

   This script will:
   - Install Poetry to C:\poetry (on Windows) or ~/.poetry (on Unix)
   - Configure Poetry to use a specific virtual environment location
   - Install all dependencies
   - Create `van_credentials.py` from the template if it doesn't exist
   - Run the installation test

2. Edit `app/van_credentials.py` to add your VAN credentials.

3. Run the VAT (Voter Analysis Tool) automation from the `app` directory:
   ```bash
   cd app
   poetry run vat
   ```

4. Additional Poetry commands:
   ```bash
   # Test the Poetry environment setup
   poetry run test-poetry
   
   # Run all tests
   poetry run pytest
   
   # Run other automation modules
   poetry run print-lists  # Vote-By-Mail list printing
   poetry run mail-prints  # Email PDFs to organizers
   ```

### Option 2: Manual Installation

If you prefer not to use Poetry, you can set up the environment manually:

1. Ensure all dependencies are installed:
   ```
   pip install -r requirements.txt
   ```

2. Make sure Chrome is installed on your system.

3. Copy `van_credentials_template.py` to `van_credentials.py` and fill in your VAN credentials:
   ```
   cp van_credentials_template.py van_credentials.py
   # Then edit van_credentials.py with your credentials
   ```

4. Run the installation test to verify everything is set up correctly:
   ```
   python test_installation.py
   ```

## Usage

Macrovan provides several automation modules that can be run independently:

### VoterData Automation

```python
from app.voter_data_automation import VoterDataAutomation

# Create the automation object
automation = VoterDataAutomation()

# Run the full process
automation.run_full_process()
```

The VAT automation will:
1. Download VoterData files from API (cached daily in io/api_downloads/)
2. Start a Chrome browser
3. Navigate to VAN and present you with the login screen
4. Wait for you to complete login and 2FA
5. Upload files to "VAT Lists (MT)" folder in VAN
6. Process all searches in "VAT Searches" folder
7. Update all lists in "VAT Lists (MT)"
8. Clean up resources

### Vote-By-Mail (VBM) Targeting

```python
from app.print_VBM_targets import run_vbm_targeting

# Run the VBM targeting process
run_vbm_targeting()
```

The VBM targeting will:
1. Read Excel input files with turf and volunteer data
2. Start a Chrome browser and log in to VoteBuilder
3. Generate lists or labels for each turf
4. Organize output PDFs by organizer
5. Clean up temporary files

## Directory Structure

```
macrovan/
├── app/                      # Main application code
│   ├── macrovat.py          # VAT automation entry point
│   ├── voter_data_automation.py    # VAT orchestration
│   ├── voter_data_downloader.py    # API downloads
│   ├── van_file_manager.py         # VAN file operations
│   ├── van_search_list_manager.py  # VAN search/list operations
│   ├── print_VBM_targets.py        # VBM list printing
│   ├── mail_in_voter_prints.py     # Email automation
│   ├── utils.py                    # Shared utilities
│   ├── van_credentials.py          # VAN login (create from template)
│   └── macrovan_config.json        # Configuration
├── io/
│   ├── api_downloads/       # Downloaded voter data files from API
│   ├── logs/                # Log files
│   └── Output/              # Generated PDFs and outputs
├── doc/                     # Documentation
└── pyproject.toml           # Poetry configuration
```

## Components

Macrovan consists of several key components:

### Core Utilities
- `utils.py`: Common utilities for browser automation, file handling, and PDF processing

### VoterData Automation
- `VoterDataDownloader`: Handles downloading VoterData files from the API
- `VANFileManager`: Manages file operations in VAN
- `VANSearchListManager`: Handles search and list operations in VAN
- `VoterDataAutomation`: Orchestrates the VoterData process

### VBM Targeting
- `print_VBM_targets.py`: Main script for VBM targeting
- `printing_steps.py`: Handles the printing workflow
- `organizer_folders.py`: Organizes output by organizer

## Testing

To run the tests:

```
pytest app/tests/
```

## Troubleshooting

Common issues:

1. **Login failures**: Ensure your VAN credentials are correct and you complete 2FA within the timeout period.

2. **Download failures**: Check your internet connection and verify the API endpoint is accessible.

3. **Upload failures**: Ensure you have the necessary permissions in VAN to upload files to the "VAT Lists (xx)" folder.

4. **Browser issues**: Make sure Chrome is installed and up to date. The automation uses ChromeDriver, which should be automatically downloaded.

5. **Poetry installation**: If you encounter issues with Poetry, ensure it's properly installed at C:\poetry (Windows) or ~/.poetry (Unix) and added to your PATH.

6. **File paths**: Some scripts may contain hardcoded file paths. Check the console output for path-related errors.

## Logging

The automation logs information to the console. You can check the logs for details about the process and any errors that occur.

## Development

To contribute to Macrovan:

1. Fork the repository
2. Install development dependencies: `poetry install --with dev`
3. Make your changes
4. Run tests: `poetry run pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.