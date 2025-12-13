# VoterData Automation

This module automates the process of downloading VoterData files, managing them in VAN, and updating saved searches and lists.

## Overview

The VoterData automation performs the following tasks:
1. Downloads 10 VoterData files (G01-G10) from the API
2. Deletes any existing VoterData files in the "VAT Lists (xx)" folder in VAN
3. Bulk uploads the downloaded files to the "VAT Lists (xx)" folder
4. Loads each search in the "VAT Searches" folder and saves the resulting list in the "VAT Lists (xx)" folder
5. Loads and saves each list in the "VAT Lists (xx)" folder to replace the bulk uploaded version

## Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`
- Chrome browser installed
- Internet connection
- VAN account with appropriate permissions

## Installation

1. Ensure all dependencies are installed:
   ```
   pip install -r requirements.txt
   ```

2. Make sure Chrome is installed on your system.

3. Copy `secrets_template.py` to `secrets.py` and fill in your VAN credentials:
   ```
   cp secrets_template.py secrets.py
   # Then edit secrets.py with your credentials
   ```

4. Run the installation test to verify everything is set up correctly:
   ```
   python test_installation.py
   ```

## Usage

To run the automation:

```python
from voter_data_automation import VoterDataAutomation

# Create the automation object
automation = VoterDataAutomation()

# Run the full process
automation.run_full_process()
```

The automation will:
1. Start a Chrome browser
2. Present you with the VAN login screen
3. Wait for you to complete the login and 2FA
4. Download the VoterData files
5. Manage the files in VAN
6. Process searches and lists
7. Clean up resources

## Components

The automation consists of the following components:

- `VoterDataDownloader`: Handles downloading VoterData files from the API
- `VANFileManager`: Manages file operations in VAN (navigation, deletion, upload)
- `VANSearchListManager`: Handles search and list operations in VAN
- `VoterDataAutomation`: Orchestrates the entire process

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

## Logging

The automation logs information to the console. You can check the logs for details about the process and any errors that occur.