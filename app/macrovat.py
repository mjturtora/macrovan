#!/usr/bin/env python
"""
Script to run the full VoterData automation process.
"""

import argparse
import os
import sys
import logging
from pathlib import Path

# 1. PATH RESOLUTION
if getattr(sys, 'frozen', False):
    # RUNNING AS EXE:
    BASE_DIR = Path(sys.executable).resolve().parent
    CODE_DIR = Path(sys._MEIPASS).resolve()  # / "app"
else:
    # RUNNING AS .PY:
    CODE_DIR = Path(__file__).resolve().parent
    BASE_DIR = CODE_DIR.parent

# Ensure the system can find 'utils' and 'voter_data_automation'
sys.path.append(str(CODE_DIR))

# 2. FOLDER GUARDIAN
# Ensures the user always has a workspace, even if they run the EXE in a new folder.
for folder in ["api_downloads", "Input", "logs", "Output"]:
    (BASE_DIR / "io" / folder).mkdir(parents=True, exist_ok=True)

from utils import load_config
from voter_data_automation import VoterDataAutomation

def setup_logging(config):
    """Set up logging using the project root as the anchor."""
    # Use BASE_DIR as the anchor so logs go to the folder next to the EXE
    log_dir = BASE_DIR / "io" / "logs"
    log_filename = config["files"]["log_files"]["macrovat"]
    log_path = log_dir / log_filename

    """Set up logging using absolute path resolution."""
    # Resolve absolute path to the logs directory relative to this script
    # rel_logs_dir = config["files"]["logs_directory"]
    # abs_logs_dir = (SCRIPT_DIR / rel_logs_dir).resolve()
    
    # Use the 'macrovat' key for the filename
    # log_filename = config["files"]["log_files"]["macrovat"]
    # log_path = abs_logs_dir / log_filename

    # Ensure the directory exists
    # log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("macrovat")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    log_cfg = config.get("logging", {})

    # 1. File Handler
    f_level_name = log_cfg.get("file_level", "INFO").upper()
    f_level = getattr(logging, f_level_name, logging.INFO)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(f_level)
    file_handler.setFormatter(formatter)

    # 2. Console Handler
    c_level_name = log_cfg.get("console_level", "INFO").upper()
    c_level = getattr(logging, c_level_name, logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(c_level)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

def main():
    """Run the VoterData automation process."""
    parser = argparse.ArgumentParser(description="Macrovan VoterData Automation")
    parser.add_argument("--all", action="store_true", help="Run the complete process")
    parser.add_argument("--searches", action="store_true", help="Run Phase 4: Refresh Searches")
    parser.add_argument("--lists", action="store_true", help="Run Phase 5: Refresh Lists")
    parser.add_argument("-f", "--files", nargs="+", help="Subset of files (e.g. -f G10 G11)")
    
    args = parser.parse_args()

    # config = load_config(SCRIPT_DIR / "macrovan_config.json")

    # FIXED: The config file is inside CODE_DIR (app folder) in both modes.
    # If we used BASE_DIR / "app", the EXE would fail because there is no "app" folder next to the .exe.
    config_path = CODE_DIR / "macrovan_config.json"
    config = load_config(config_path)

    logger = setup_logging(config)
    
    logger.info("Starting VoterData automation process")

    try:
        # Pass the FULL path to the orchestrator so it doesn't rely on the current directory.
        automation = VoterDataAutomation(
            config_path=str(config_path), 
            file_override=args.files
        )

        # 1. Handle the "Run Everything" case (The Default)
        if args.all or not (args.searches or args.lists):
            logger.info("Executing full VoterData automation process")
            automation.run_full_process()
            return 0

        # 2. Handle specific phases (Allows combining --searches and --lists)
        if args.searches or args.lists:
            automation.initialize_browser()
            
            if args.searches:
                logger.info("Executing Phase 4: Refresh Searches")
                automation.refresh_searches()
                
            if args.lists:
                logger.info("Executing Phase 5: Refresh Lists")
                automation.refresh_lists()

        return 0

    except Exception as e:
        logger.error(f"Error in automation process: {e}")
        return 1
        
    finally:
        # Ensure cleanup runs regardless of execution path
        if 'automation' in locals():
            automation.cleanup()

if __name__ == "__main__":
    print(f"[*] Execution Dir: {os.getcwd()}")
    # We use BASE_DIR here to show where the user's files will be generated
    print(f"[*] Project Root:  {BASE_DIR}")
    exit_code = main() # Run the main function