#!/usr/bin/env python
"""
todo: Need to add a test for the case where the named file is not found and van displays:
No Results Found
Try broadening your search.


Live integration test for deleting files from VAN.

This test actually connects to VoteBuilder and deletes files.
Use with caution - it performs real deletions on the live system.

Usage:
    cd app
    poetry run pytest tests/test_live_delete.py -s
"""

import sys
import os
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voter_data_automation import VoterDataAutomation


def test_delete_files(num_files=3):
    """
    Live test: Delete num_files files from VAN using the existing automation infrastructure.
    
    This test leverages the VoterDataAutomation class to:
    1. Load configuration from macrovan_config.json
    2. Initialize browser and login
    3. Delete only the first num_files files from the configured file_ids
    4. Clean up
    
    Note: This deletes REAL files. Only run when those files exist and 
    should be deleted.
    """
    automation = None
    
    try:
        # Initialize automation (loads config, sets up logging)
        automation = VoterDataAutomation(config_path="macrovan_config.json")
        
        # Get configuration values
        list_folder = automation.config["van"]["folders"]["list_folder"]
        all_file_ids = automation.config["api"]["file_ids"]
        
        # TEST MODIFICATION: Only use first num_files files instead of all 10
        test_file_ids = all_file_ids[:num_files]
        
        automation.logger.info("=" * 60)
        automation.logger.info("LIVE DELETE TEST - WILL DELETE REAL FILES")
        automation.logger.info(f"Using config: macrovan_config.json")
        automation.logger.info(f"Target folder: {list_folder}")
        automation.logger.info(f"All configured files: {all_file_ids}")
        automation.logger.info(f"Test will delete only: {test_file_ids}")
        automation.logger.info("=" * 60)
        
        # Use existing method to initialize browser and login
        automation.logger.info("Initializing browser and logging in...")
        automation.initialize_browser()
        
        # Navigate to the list folder
        automation.logger.info(f"Navigating to {list_folder}...")
        automation.file_manager.navigate_to_file_folder(list_folder)
        
        # Delete only the test files (first num_files)
        file_patterns = [f"{file_id}_VoterData" for file_id in test_file_ids]
        automation.logger.info(f"Deleting files: {file_patterns}")
        automation.file_manager.delete_files(file_patterns)
        
        automation.logger.info("=" * 60)
        automation.logger.info("TEST COMPLETED SUCCESSFULLY")
        automation.logger.info("=" * 60)
        
        # Pause to allow visual inspection
        import time
        automation.logger.info("Pausing 5 seconds for visual inspection...")
        time.sleep(5)
        
    except Exception as e:
        if automation:
            automation.logger.error(f"Test failed with error: {e}")
        raise
        
    finally:
        # Use existing cleanup method
        if automation:
            automation.cleanup()


if __name__ == "__main__":
    """Allow running directly: python tests/test_live_delete.py"""
    test_delete_files(num_files=10)
