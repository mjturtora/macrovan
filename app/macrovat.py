#!/usr/bin/env python
"""
Script to run the full VoterData automation process.

This script uses the VoterDataAutomation class to run the full process of
downloading VoterData files, managing them in VAN, and processing searches and lists.
"""

import os
import sys
import json
import logging

# Add the current script's directory (app/) to the search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth import username, password
from voter_data_automation import VoterDataAutomation

def load_config(config_path="macrovan_config.json"):
    """
    Load configuration from a JSON file.
    
    Args:
        config_path (str): Path to the configuration file.
        
    Returns:
        dict: The configuration.
        
    Raises:
        FileNotFoundError: If the configuration file is not found.
        json.JSONDecodeError: If the configuration file is not valid JSON.
    """
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file is not found, try looking in the same directory as this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, config_path)
        with open(config_path, 'r') as f:
            return json.load(f)

def setup_logging(config):
    """Set up logging with independent levels for console and file."""
    log_path = os.path.join(
        config["files"]["logs_directory"],
        config["files"]["log_files"]["macrovat"]
    )
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger = logging.getLogger("macrovat")
    
    # Set the master logger to DEBUG so it doesn't throttle the handlers
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_cfg = config.get("logging", {})

    # 1. Configure File Handler
    f_level_str = log_cfg.get("file_level", "INFO").upper()
    f_level = getattr(logging, f_level_str, logging.INFO)
    
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(f_level)
    file_handler.setFormatter(formatter)

    # 2. Configure Console Handler
    c_level_str = log_cfg.get("console_level", "INFO").upper()
    c_level = getattr(logging, c_level_str, logging.INFO)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(c_level)
    console_handler.setFormatter(formatter)

    # 3. Attach Handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

def main():
    """Run the full VoterData automation process."""
    # Load configuration
    config = load_config()
    
    # Setup logging with config
    logger = setup_logging(config)
    
    logger.info("Starting full VoterData automation process")
    
    try:
        # Initialize the automation
        automation = VoterDataAutomation(config_path="macrovan_config.json")
        
        # Run the full process
        automation.run_full_process()
        
        logger.info("Full VoterData automation process completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error in automation process: {e}")
        return 1

if __name__ == "__main__":
    print(f"[*] Execution Dir: {os.getcwd()}")
    print(f"[*] Python Path:   {sys.path[0]}")
    exit_code = main()
    exit(exit_code)