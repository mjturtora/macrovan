# MacroVan

MacroVan is a Robotic Process Automation (RPA) toolkit designed to automate voter data management, campaign operations, and volunteer coordination.

## 🎮 Quick Usage Reference

Run these commands from the project root folder using Poetry.

| Command | Description |
| :--- | :--- |
| `poetry run vat` | **Main Automation:** Full 6-phase pipeline for all file IDs in config. |
| `poetry run vat -f G10 G11` | **Targeted Run:** Process only specific file IDs (subsetting). |
| `poetry run vat --lists -f G10` | **Targeted Fix:** Refresh only Phase 6 for a specific file. |
| `poetry run vat --reset` | **Credential Management:** Change or reset saved VAN credentials. |
| `poetry run vat --searches` | **Phase 5 Only:** Refresh saved searches and save to lists. |
| `poetry run vat --lists` | **Phase 6 Only:** Refresh existing VoterData lists. |
| `poetry run print-lists` | **VBM Targeting:** Process and print target lists from Excel. |
| `poetry run mail-prints` | **Distribution:** Email generated PDFs to organizers. |
| `poetry run pytest` | **Testing:** Run the internal test suite. |

---

## 🚀 Overview
MacroVan automates critical campaign operations using Selenium and the system keyring for secure credential management.

* **VAT Automation:** Manages a 6-phase pipeline: API Download, Browser Init, VAN Cleanup, VAN Upload, Search Refresh, and List Refresh.
* **Targeted Execution:** Supports the `-f` / `--files` flag to subset operations, allowing for rapid recovery from "Oops" errors or specific file updates without re-running the entire set.
* **Canvas List Printing:** Prints lists from selected folders in VAN and labels from Excel inputs.
* **Vote-By-Mail (VBM) Targeting:** Automates printing of Vote-By-Mail target lists.
* **Email Distribution:** Emails generated PDFs to organizers based on Excel lists.
* **PDF Processing:** Extracts information from generated PDFs, organizes output by organizer, and manages file cleanup.
* **Secure Auth:** Uses **Windows Credential Manager** or **macOS Keychain** (via `keyring`) to eliminate plain-text password files.
* **Credential Configuration:** The script proactively prompts for username/password on the first run. To update later, use the `--reset` flag.
* **Standalone Executables:** Includes GitHub Actions workflows to compile cross-platform (Mac/Windows) binaries for non-technical users.

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

## 📦 Building Executables

For users without Python installed, you can compile standalone executables using the included GitHub Actions workflows.

1. Navigate to the **Actions** tab on your GitHub repository (or use the VS Code GitHub Actions extension).
2. Select either the **Build Mac Executable** or **Build Cross-Platform Executables** workflow from the sidebar.
3. Click **Run workflow**.
4. Once completed, download the `.exe` (Windows) or Unix executable (Mac) from the Artifacts section at the bottom of the run summary.

### **Running on macOS (The "Manual Override")**
Because the Mac binary is unsigned, Apple's **Gatekeeper** will block the first launch. Use one of the following methods to "bless" the app:

#### **Method 1: Right-Click (Easiest)**
1. Download and **Unzip** the `MacroVan-MacOS.zip` file.
2. **Do not double-click the app.** Instead, **Right-Click** the `MacroVan` file and select **Open**.
3. A dialog will appear saying "macOS cannot verify the developer." Click **Open** again.

#### **Method 2: System Settings**
1. If the app fails to open, go to **System Settings** > **Privacy & Security**.
2. Scroll down to the **Security** section.
3. You will see a message: "MacroVan was blocked from use because it is not from an identified developer."
4. Click **Open Anyway**.

#### **Method 3: The Terminal (Nuclear Option)**
If the above fails, open Terminal in the app's folder and run:
```bash
xattr -d com.apple.quarantine MacroVan
```

---

## 📁 Project Structure

```text
macrovan/
├── .github/                       # GitHub Actions CI/CD
│   └── workflows/                 # Compilation workflows (Mac, Cross-Platform)
├── app/                           # Main application code
│   ├── auth.py                    # Secure Keyring Bridge
│   ├── macrovat.py                # VAT automation entry point
│   ├── voter_data_automation.py   # VAT orchestration & subsetting
│   ├── voter_data_downloader.py   # API data retrieval
│   ├── van_file_manager.py        # Browser-based file handling & polling
│   ├── print_VBM_targets.py       # Vote-By-Mail list printing
│   ├── mail_in_voter_prints.py    # Email automation for organizers
│   ├── utils.py                   # Shared Selenium & PDF utilities
│   └── macrovan_config.json       # JSON configuration for file paths/logs
├── chrome-data/                   # Persistent browser sessions
│   └── .wdm/                      # Driver cache
├── io/                            # Data Input/Output (Anchored via pathlib)
│   ├── api_downloads/             # Cached VoterData from API
│   ├── Input/                     # Source spreadsheets and trackers
│   ├── logs/                      # Application log files
│   └── Output/                    # Generated PDFs and distribution folders
├── pyproject.toml                 # Poetry environment & dependencies
├── refresh_binaries.ps1           # Trigger GitHub build workflow
└── setup_environment.bat          # Automated setup script
```

---

## 🛠️ Developer Note: Path Anchoring
To ensure the toolkit is location-independent (Poetry vs. EXE), all entry points must anchor to the **Project Root (base_dir)**. This ensures that logs and data folders land in the same location regardless of where the code is stored.

```python
from pathlib import Path
import sys

if getattr(sys, 'frozen', False):
    # Running as a bundled EXE
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # Running as a script (anchors to folder above 'app/')
    BASE_DIR = Path(__file__).resolve().parent.parent
```
*Note: As of March 2026, the VAT pipeline is the primary implementation of this cross-platform standard.*

---

## 🔧 Troubleshooting

* **Targeted Retries:** If a file fails during Phase 6 (List Refresh), use: `poetry run vat --lists -f [FileID]`.
* **2FA Timeout:** Selenium will wait at the login screen for you to complete the 2FA prompt manually.
* **NumPy/Pandas Conflict:** This project pins `numpy < 2.0` to maintain compatibility with Pandas.
* **VAN "Oops":** Often caused by server-side timeouts. `VANFileManager` includes polling logic to wait for "100% Processed" status. Check `vat_automation.log` for poll results.

---

## ⚖️ License

This project is licensed under the MIT License.