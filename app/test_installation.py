#!/usr/bin/env python
"""
Script to test the installation and dependencies for the VoterData automation.

This script checks that all required dependencies are installed and working.
"""

import sys
import importlib
import logging

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger("test_installation")

def check_dependency(logger, module_name, import_name=None):
    """
    Check if a dependency is installed and working.
    
    Args:
        logger: The logger to use.
        module_name (str): The name of the module to import.
        import_name (str, optional): The name to import from the module.
            If None, the module itself is imported.
    
    Returns:
        bool: True if the dependency is installed and working, False otherwise.
    """
    try:
        if import_name:
            # Import a specific name from the module
            module = importlib.import_module(module_name)
            getattr(module, import_name)
            logger.info(f"[+] Successfully imported {import_name} from {module_name}")
        else:
            # Import the module itself
            importlib.import_module(module_name)
            logger.info(f"[+] Successfully imported {module_name}")
        return True
    except ImportError:
        logger.error(f"[-] Failed to import {module_name}")
        return False
    except AttributeError:
        logger.error(f"[-] Failed to import {import_name} from {module_name}")
        return False

def check_file_exists(logger, file_path):
    """
    Check if a file exists.
    
    Args:
        logger: The logger to use.
        file_path (str): The path to the file to check.
    
    Returns:
        bool: True if the file exists, False otherwise.
    """
    import os
    if os.path.exists(file_path):
        logger.info(f"[+] File exists: {file_path}")
        return True
    else:
        logger.error(f"[-] File does not exist: {file_path}")
        return False

def main():
    """Run the installation test."""
    logger = setup_logging()
    
    logger.info("Testing installation and dependencies...")
    
    # Check core dependencies
    dependencies = [
        ("selenium", None),
        ("selenium.webdriver", "Chrome"),
        ("selenium.webdriver.chrome.options", "Options"),
        ("selenium.webdriver.common.by", "By"),
        ("selenium.webdriver.support.ui", "WebDriverWait"),
        ("selenium.webdriver.support.expected_conditions", None),
        ("webdriver_manager.chrome", "ChromeDriverManager"),
        ("requests", None),
        ("pandas", None),
        ("PyPDF2", None),
        ("json", None),
        ("os", None),
        ("sys", None),
        ("logging", None),
    ]
    
    all_dependencies_ok = True
    for module_name, import_name in dependencies:
        if not check_dependency(logger, module_name, import_name):
            all_dependencies_ok = False
    
    # Check project files
    project_files = [
        "utils.py",
        "voter_data_automation.py",
        "voter_data_downloader.py",
        "van_file_manager.py",
        "van_search_list_manager.py",
        "macrovan_config.json",
    ]
    
    all_files_ok = True
    for file_path in project_files:
        if not check_file_exists(logger, file_path):
            all_files_ok = False
    
    # Print summary
    if all_dependencies_ok and all_files_ok:
        logger.info("[SUCCESS] All dependencies and files are installed and working!")
        return 0
    else:
        logger.error("[ERROR] Some dependencies or files are missing or not working.")
        return 1

if __name__ == "__main__":
    sys.exit(main())