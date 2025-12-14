#!/usr/bin/env python
"""
Script to run the full VoterData automation process.

This script uses the VoterDataAutomation class to run the full process of
downloading VoterData files, managing them in VAN, and processing searches and lists.
"""

import os
import json
import logging
from voter_data_automation import VoterDataAutomation

def load_config(config_path="voter_data_config.json"):
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
    """Set up logging configuration."""
    log_path = os.path.join(
        config["files"]["logs_directory"],
        config["files"]["log_files"]["run_voter_data_automation"]
    )
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("run_voter_data_automation")

def main():
    """Run the full VoterData automation process."""
    # Load configuration
    config = load_config()
    
    # Setup logging with config
    logger = setup_logging(config)
    
    logger.info("Starting full VoterData automation process")
    
    try:
        # Initialize the automation
        automation = VoterDataAutomation(config_path="voter_data_config.json")
        
        # Run the full process
        automation.run_full_process()
        
        logger.info("Full VoterData automation process completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error in automation process: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)