#!/usr/bin/env python
"""
Script to download VoterData files from the API.

This script uses the VoterDataDownloader class to download VoterData files
from the API and save them to the specified output directory.
"""

import os
import json
import logging
from voter_data_downloader import VoterDataDownloader

def setup_logging(config):
    """Set up logging configuration."""
    log_path = os.path.join(
        config["files"]["logs_directory"],
        config["files"]["log_files"]["vat_downloader"]
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
    return logging.getLogger("download_voter_data")

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

def main():
    """Run the download process."""
    # Load configuration
    config = load_config()
    
    # Setup logging with config
    logger = setup_logging(config)
    
    logger.info("Starting VoterData download process")
    
    try:
        
        # Create downloader
        downloader = VoterDataDownloader(
            base_url=config["api"]["base_url"],
            output_directory=config["files"]["output_directory"]
        )
        
        # Get file IDs from config
        file_ids = config["api"]["file_ids"]
        
        # Download all files
        logger.info(f"Downloading {len(file_ids)} files: {file_ids}")
        downloaded_files = downloader.download_all_files(file_ids)
        
        logger.info(f"Successfully downloaded {len(downloaded_files)} files:")
        for file_path in downloaded_files:
            logger.info(f"  - {file_path}")
        
        return 0
    except Exception as e:
        logger.error(f"Error in download process: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)