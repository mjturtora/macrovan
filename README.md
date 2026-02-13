# MacroVan

MacroVan is a Robotic Process Automation (RPA) toolkit designed to automate voter data management, campaign operations, and volunteer coordination.

## 🎮 Quick Usage Reference

Run these commands from the project app folder using Poetry.

| Command | Description |
| :--- | :--- |
| `poetry run vat` | **Main Automation:** Downloads files, uploads to VAN, and updates lists. |
| `poetry run vat --reset` | **Credential Management:** Change or reset saved VAN username/password. |
| `poetry run print-lists` | **VBM Targeting:** Process and print target lists from Excel. |
| `poetry run mail-prints` | **Distribution:** Email generated PDFs to organizers. |
| `poetry run pytest` | **Testing:** Run the internal test suite. |

---

## 🚀 Overview
MacroVan automates critical campaign operations using Selenium and the system keyring for secure credential management.

* **VAT Automation:** Downloads VoterData (G01-G10), manages bulk uploads to VAN, and processes "VAT Searches."
* **Canvas list printing**: Prints lists from selected folders in VAN and labels from Excel inputs.
* **Vote-By-Mail (VBM) Targeting:** Automates printing of Vote-By-Mail target lists
* **email distribution:** Emails generated PDFs to organizers based Excel lists.
* **PDF Processing:** Extracts information from generated PDFs, organizes output by organizer, and manages file cleanup.
* **Secure Auth:** Uses **Windows Credential Manager** (via `keyring`) to eliminate plain-text password files. The script will print `[*] Active User: [name]` at startup.
* **Credential Configuration:** The script will proactively prompt you for your username and password on the first run and save them securely to your OS. To update them later, use the ```--reset``` flag shown in the Usage section.

---

## 🛠️ Requirements
* **Python 3.11+**
* **Poetry** (Dependency management)
* **Google Chrome** (For Selenium automation)
* **VAN Account** with appropriate permissions

---

## 📥 Installation

### Environment Setup
Run the automated setup script to install dependencies and configure the virtual environment:

**Windows:**
```powershell
./setup_environment.bat
```
**macOS/Linux:**
```bash
chmod +x setup_environment.sh
./setup_environment.sh
```
---
## 📁 Project Structure

```text
macrovan/
├── app/                           # Main application code
│   ├── auth.py                    # Secure Keyring Bridge (Replaces credentials file)
│   ├── macrovat.py                # VAT automation entry point
│   ├── voter_data_automation.py   # VAT orchestration logic
│   ├── voter_data_downloader.py   # API data retrieval
│   ├── van_file_manager.py        # Browser-based file handling in VAN
│   ├── van_search_list_manager.py # Saved search and list processing
│   ├── print_VBM_targets.py       # Vote-By-Mail list printing
│   ├── mail_in_voter_prints.py    # Email automation for organizers
│   ├── utils.py                   # Shared Selenium & PDF utilities
│   └── macrovan_config.json       # JSON configuration for file paths/logs
├── io/                            # Data Input/Output
│   ├── api_downloads/             # Cached VoterData from API
│   ├── logs/                      # Application log files
│   └── Output/                    # Generated PDFs and distribution folders
├── pyproject.toml                 # Poetry environment & dependencies
└── setup_environment.bat          # Automated setup script
```




---

## 🔧 Troubleshooting

* **2FA Timeout:** You must be present to complete the 2FA prompt in the Chrome window during the login phase.
* **NumPy/Pandas Conflict:** This project pins ```numpy < 2.0``` to maintain binary compatibility with the current Pandas version.
* **Chromedriver:** Handled automatically by Selenium; ensure your Chrome browser is up to date.

---

## ⚖️ License

This project is licensed under the MIT License.

---
