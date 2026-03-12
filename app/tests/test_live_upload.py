#!/usr/bin/env python
"""
Live integration test for uploading files to VAN (default: 3 files).

This test connects to VoteBuilder and uploads files from local storage.
Use with caution - it performs real uploads on the live system.

Usage:
    cd app
    poetry run pytest tests/test_live_upload.py -s
"""

import sys
import os
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voter_data_automation import VoterDataAutomation


def test_upload_files(num_files=3):
    """
    Live test: Upload test files to VAN from local storage.
    
    This test leverages the VoterDataAutomation class to:
    1. Load configuration from macrovan_config.json
    2. Initialize browser and login
    3. Upload test CSV files from api_downloads directory
    4. Clean up
    
    Note: This uploads REAL files to the live VAN system.
    """
    automation = None
    
    try:
        # Initialize automation (loads config, sets up logging)
        automation = VoterDataAutomation(config_path="macrovan_config.json")
        
        # Get configuration values
        list_folder = automation.config["van"]["folders"]["list_folder"]
        all_file_ids = automation.config["api"]["file_ids"]
        downloads_dir = automation.config["files"]["output_directory"]
        
        # TEST MODIFICATION: Only use first num_files files instead of all 10
        test_file_ids = all_file_ids[:num_files]
        
        # Build file paths from local storage
        file_paths = []
        for file_id in test_file_ids:
            file_path = os.path.abspath(os.path.join(downloads_dir, f"{file_id}_VoterData.csv"))
            if os.path.exists(file_path):
                file_paths.append(file_path)
                automation.logger.info(f"Found file: {file_path}")
            else:
                automation.logger.warning(f"File not found: {file_path}")
        
        if not file_paths:
            automation.logger.error("No files found to upload!")
            raise FileNotFoundError("No CSV files found in api_downloads directory")
        
        automation.logger.info("=" * 60)
        automation.logger.info("LIVE UPLOAD TEST - WILL UPLOAD REAL FILES")
        automation.logger.info(f"Using config: macrovan_config.json")
        automation.logger.info(f"Target folder: {list_folder}")
        automation.logger.info(f"Files to upload: {file_paths}")
        automation.logger.info("=" * 60)
        
        # Use existing method to initialize browser and login
        automation.logger.info("Initializing browser and logging in...")
        automation.initialize_browser()
        
        # Navigate to the list folder
        automation.logger.info(f"Navigating to {list_folder}...")
        automation.file_manager.navigate_to_file_folder(list_folder)
        
        # Upload the files
        automation.logger.info(f"Uploading {len(file_paths)} files...")
        automation.file_manager.bulk_upload_files(file_paths)
        
        # Verify upload
        if automation.file_manager.verify_upload_success():
            automation.logger.info("Upload verified as successful")
        else:
            automation.logger.warning("Could not verify upload success")
        
        automation.logger.info("=" * 60)
        automation.logger.info("TEST COMPLETED SUCCESSFULLY")
        automation.logger.info("=" * 60)
        
        # Pause to allow visual inspection
        import time
        automation.logger.info("Pausing 10 seconds for visual inspection...")
        time.sleep(10)
        
    except Exception as e:
        if automation:
            automation.logger.error(f"Test failed with error: {e}")
        raise
        
    finally:
        # Use existing cleanup method
        if automation:
            automation.cleanup()


if __name__ == "__main__":
    """Allow running directly: poetry run python tests/test_live_upload.py"""
    test_upload_files(num_files=3)
