#!/usr/bin/env python
"""
macrovat: A specialized VAN automation macro for VoterData.

This application acts as a specialized 'macro' within the broader macrovan 
automation framework. It manages the full lifecycle of VoterData—from 
API retrieval to VAN synchronization—ensuring data remains fresh and accurate.
"""

# 1. Standard Library Imports
import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# 2. Path Resolution
# We define two distinct realms:
# The 'Village' (BASE_DIR): Where the user lives, sees logs, and edits config.
# The 'Keep' (CODE_DIR): Where the internal program logic is hidden.
if getattr(sys, 'frozen', False):
    # Running as a bundled EXE
    BASE_DIR = Path(sys.executable).resolve().parent
    CODE_DIR = Path(sys._MEIPASS).resolve()
else:
    # Running as a standard Python script
    CODE_DIR = Path(__file__).resolve().parent
    BASE_DIR = CODE_DIR.parent

# Anchor the system to find our internal modules before importing them
sys.path.append(str(CODE_DIR))

# 3. Local Application Imports
from utils import load_config
from voter_data_automation import VoterDataAutomation


def setup_logging(config):
    """Configures the app's diary (logs) so we can track its progress."""
    # Ensure logs stay in the 'Village' so they are easily accessible to the user
    log_dir = BASE_DIR / "io" / "logs"
    log_filename = config["files"]["log_files"]["macrovat"]
    log_path = log_dir / log_filename

    logger = logging.getLogger("macrovat")
    logger.propagate = False 
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    log_cfg = config.get("logging", {})

    # File Logging: A permanent record of every run
    f_level = getattr(logging, log_cfg.get("file_level", "INFO").upper(), logging.INFO)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(f_level)
    file_handler.setFormatter(formatter)

    # Console Logging: Real-time feedback in the terminal window
    c_level = getattr(logging, log_cfg.get("console_level", "INFO").upper(), logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(c_level)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def main():
    """Main entry point for the macrovat automation process."""
    
    # --- STEP A: Infrastructure Setup ---
    # Create the 'Village' folders if they don't exist yet.
    for folder in ["api_downloads", "logs", "inputs"]:
        (BASE_DIR / "io" / folder).mkdir(parents=True, exist_ok=True)

    # --- STEP B: The Scavenger Hunt ---
    # Look for a user-edited config in the 'Village', fall back to the internal one.
    external_config = BASE_DIR / "io" / "inputs" / "macrovan_config.json"
    internal_config = CODE_DIR / "macrovan_config.json"

    if external_config.exists():
        # Syntax Check: Ensure the user's custom file isn't corrupted (e.g., missing commas)
        try:
            with open(external_config, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"[*] Using CUSTOM configuration: {external_config}")
            config_path = external_config
        except json.JSONDecodeError as e:
            print(f"[!] FATAL ERROR: Your custom JSON file has a syntax error: {e}")
            return 1
    else:
        # Bootstrap: Create a template from the internal settings for the user
        print(f"[!] Custom config not found. Bootstrapping template to (external_config): {external_config}")
        factory_settings = load_config(internal_config)
        with open(external_config, 'w', encoding='utf-8') as f:
            print(f"[*] Writing new config from (internal_config) {internal_config}")
            json.dump(factory_settings, f, indent=2)
        config_path = external_config

    # --- STEP C: Initialization ---
    config = load_config(config_path)
    logger = setup_logging(config)
    start_time = datetime.now()
    
    parser = argparse.ArgumentParser(description="macrovat: VoterData Automation")
    parser.add_argument("--all", action="store_true", help="Run the full 6-phase pipeline")
    parser.add_argument("--searches", action="store_true", help="Run Phase 5: Refresh Searches")
    parser.add_argument("--lists", action="store_true", help="Run Phase 6: Refresh Lists")
    parser.add_argument("-f", "--files", nargs="+", help="Subset of files (e.g. -f G10 G11)")
    args = parser.parse_args()

    logger.info("Starting macrovat automation process")

    try:
        # Pass the config as a string to maintain Pylance compatibility
        automation = VoterDataAutomation(
            config_path=str(config_path), 
            file_override=args.files
        )

        # Execution logic based on user flags
        if args.all or not (args.searches or args.lists):
            logger.info("Executing full end-to-end automation")
            automation.run_full_process()
        else:
            automation.initialize_browser()
            if args.searches:
                automation.refresh_searches()
            if args.lists:
                automation.refresh_lists()

        # --- STEP D: Completion Summary ---
        # Capture stats from the orchestrator for the final log entry
        end_time = datetime.now()
        duration = str(end_time - start_time).split('.')[0]
        stats = automation.stats
        
        summary = (
            f"SUMMARY: Duration: {duration} | "
            f"Retrieved: {stats['files_downloaded']} | "
            f"Cleaned: {stats['files_deleted']} | "
            f"Uploaded: {stats['files_uploaded']} | "
            f"Searches: {stats['searches_refreshed']} | "
            f"Lists: {stats['lists_refreshed']}"
        )

        logger.info("-" * 50)
        logger.info("Automation process finished successfully.")
        logger.info(summary)
        logger.info("-" * 50)
        return 0

    except Exception as e:
        logger.error(f"Critical error during automation: {e}")
        return 1
    finally:
        # Safely shut down the browser
        if 'automation' in locals():
            automation.cleanup()


if __name__ == "__main__":
    # Launch the app and return the final status to the system
    sys.exit(main())