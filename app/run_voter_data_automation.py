#!/usr/bin/env python
"""
Script to run the VoterData automation process.

This script downloads VoterData files from the API, manages them in VAN,
and processes searches and lists.
"""

import logging
import sys
import traceback
from voter_data_automation import VoterDataAutomation

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("voter_data_automation.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Run the VoterData automation process."""
    setup_logging()
    logger = logging.getLogger("run_voter_data_automation")
    
    logger.info("Starting VoterData automation")
    
    try:
        # Create the automation object
        automation = VoterDataAutomation()
        
        # Run the full process
        automation.run_full_process()
        
        logger.info("VoterData automation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error in VoterData automation: {e}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())