# MacroVan

MacroVan is a Robotic Process Automation (RPA) toolkit designed to automate voter data management, campaign operations, and volunteer coordination.

## 🎮 Quick Usage Reference

Run these commands from the project root folder using Poetry.

| Command | Description |
| :--- | :--- |
| `poetry run vat` | **Main Automation:** Full 5-phase pipeline for all file IDs in config. |
| `poetry run vat -f G10 G11` | **Targeted Run:** Process only specific file IDs (subsetting). |
| `poetry run vat --lists -f G10` | **Targeted Fix:** Refresh only Phase 5 for a specific file. |
| `poetry run vat --reset` | **Credential Management:** Change or reset saved VAN credentials. |
| `poetry run vat --searches` | **Phase 4 Only:** Refresh saved searches and save to lists. |
| `poetry run vat --lists` | **Phase 5 Only:** Refresh existing VoterData lists. |
| `poetry run print-lists` | **VBM Targeting:** Process and print target lists from Excel. |
| `poetry run mail-prints` | **Distribution:** Email generated PDFs to organizers. |
| `poetry run pytest` | **Testing:** Run the internal test suite. |

---

## 🚀 Overview
MacroVan automates critical campaign operations using Selenium and the system keyring for secure credential management.

* **VAT Automation:** Manages a 5-phase pipeline: API Download, Browser Init, VAN Upload, Search Refresh, and List Refresh.
* **Targeted Execution:** Supports the `-f` / `--files` flag to subset operations, allowing for rapid recovery from "Oops" errors or specific file updates without re-running the entire set.
* **Canvas List Printing:** Prints lists from selected folders in VAN and labels from Excel inputs.
* **Vote-By-Mail (VBM) Targeting:** Automates printing of Vote-By-Mail target lists.
* **Email Distribution:** Emails generated PDFs to organizers based on Excel lists.
* **PDF Processing:** Extracts information from generated PDFs, organizes output by organizer, and manages file cleanup.
* **Secure Auth:** Uses **Windows Credential Manager** (via `keyring`) to eliminate plain-text password files.
* **Credential Configuration:** The script proactively prompts for username/password on the first run. To update later, use the `--reset` flag.

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
│   ├── auth.py                    # Secure Keyring Bridge
│   ├── macrovat.py                # VAT automation entry point
│   ├── voter_data_automation.py   # VAT orchestration & subsetting
│   ├── voter_data_downloader.py   # API data retrieval
│   ├── van_file_manager.py        # Browser-based file handling & polling
│   ├── print_VBM_targets.py       # Vote-By-Mail list printing
│   ├── mail_in_voter_prints.py    # Email automation for organizers
│   ├── utils.py                   # Shared Selenium & PDF utilities
│   └── macrovan_config.json       # JSON configuration for file paths/logs
├── io/                            # Data Input/Output (Anchored via pathlib)
│   ├── api_downloads/             # Cached VoterData from API
│   ├── Input/                     # Source spreadsheets and trackers
│   ├── logs/                      # Application log files
│   └── Output/                    # Generated PDFs and distribution folders
├── pyproject.toml                 # Poetry environment & dependencies
└── setup_environment.bat          # Automated setup script
```

---

## 🛠️ Developer Note: Path Anchoring
To ensure the toolkit is location-independent (Poetry vs. direct execution), all entry points must anchor their execution context to the script's physical location using `pathlib`:

```python
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))
```
*Note: As of March 2026, the VAT pipeline is the primary implementation of this cross-platform standard.*

---

## 🔧 Troubleshooting

* **Targeted Retries:** If a file fails during Phase 5 (List Refresh), use: `poetry run vat --lists -f [FileID]`.
* **2FA Timeout:** Selenium will wait at the login screen for you to complete the 2FA prompt manually.
* **NumPy/Pandas Conflict:** This project pins `numpy < 2.0` to maintain compatibility with Pandas.
* **VAN "Oops":** Often caused by server-side timeouts. `VANFileManager` includes polling logic to wait for "100% Processed" status. Check `vat_automation.log` for poll results.

---

## ⚖️ License

This project is licensed under the MIT License.