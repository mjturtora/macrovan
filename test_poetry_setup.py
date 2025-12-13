#!/usr/bin/env python
"""
Script to test that the Poetry environment is set up correctly.

This script checks that all required dependencies are installed and working
in the Poetry environment.
"""

import sys
import importlib
import subprocess
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
    return logging.getLogger("test_poetry_setup")

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
            logger.info(f"✓ Successfully imported {import_name} from {module_name}")
        else:
            # Import the module itself
            importlib.import_module(module_name)
            logger.info(f"✓ Successfully imported {module_name}")
        return True
    except ImportError:
        logger.error(f"✗ Failed to import {module_name}")
        return False
    except AttributeError:
        logger.error(f"✗ Failed to import {import_name} from {module_name}")
        return False

def check_poetry_environment(logger):
    """
    Check that we're running in a Poetry environment.
    
    Returns:
        bool: True if we're in a Poetry environment, False otherwise.
    """
    try:
        # Run 'poetry env info' to check if we're in a Poetry environment
        result = subprocess.run(
            ["poetry", "env", "info"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        logger.info("✓ Running in a Poetry environment")
        logger.info(result.stdout)
        return True
    except subprocess.CalledProcessError:
        logger.error("✗ Not running in a Poetry environment")
        return False
    except FileNotFoundError:
        logger.error("✗ Poetry is not installed or not in PATH")
        return False

def main():
    """Run the Poetry environment test."""
    logger = setup_logging()
    
    logger.info("Testing Poetry environment setup...")
    
    # Check that we're running in a Poetry environment
    if not check_poetry_environment(logger):
        logger.error("Please run this script within a Poetry environment.")
        logger.error("You can activate the Poetry environment with 'poetry shell'")
        logger.error("or run this script with 'poetry run python test_poetry_setup.py'")
        return 1
    
    # Check core dependencies
    dependencies = [
        ("selenium", None),
        ("selenium.webdriver", "Chrome"),
        ("selenium.webdriver.chrome.options", "Options"),
        ("selenium.webdriver.common.by", "By"),
        ("selenium.webdriver.support.ui", "WebDriverWait"),
        ("selenium.webdriver.support", "expected_conditions"),
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
    
    # Print summary
    if all_dependencies_ok:
        logger.info("✅ Poetry environment is set up correctly!")
        return 0
    else:
        logger.error("❌ Some dependencies are missing or not working.")
        logger.error("Try running 'poetry install' to install all dependencies.")
        return 1

if __name__ == "__main__":
    sys.exit(main())