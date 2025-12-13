import os
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import utils

class VANFileManager:
    """
    A class for managing files in the VAN interface.
    
    This class handles operations related to file management in VAN, including
    navigating to file folders, deleting files, uploading files, and verifying
    upload success.
    """
    
    def __init__(self, driver):
        """
        Initialize the VANFileManager.
        
        Args:
            driver: The Selenium WebDriver instance to use for browser automation.
        """
        self.driver = driver
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('VANFileManager')
    
    def navigate_to_file_folder(self, folder_name):
        """
        Navigate to a specific folder in VAN.
        
        Args:
            folder_name (str): The name of the folder to navigate to.
        
        Raises:
            TimeoutException: If the folder element cannot be found.
        """
        self.logger.info(f"Navigating to folder: {folder_name}")
        
        try:
            # Find and click the folder link
            folder_element = utils.expect_by_XPATH(
                self.driver, 
                f"//a[contains(text(), '{folder_name}')]"
            )
            folder_element.click()
            self.logger.info(f"Successfully navigated to folder: {folder_name}")
        except TimeoutException as e:
            self.logger.error(f"Timeout while navigating to folder {folder_name}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error navigating to folder {folder_name}: {e}")
            raise
    
    def delete_files(self, file_patterns):
        """
        Delete files in VAN that match the specified patterns.
        
        Args:
            file_patterns (list): A list of file name patterns to match for deletion.
        
        Raises:
            TimeoutException: If elements cannot be found.
            NoSuchElementException: If elements cannot be found.
        """
        self.logger.info(f"Deleting files matching patterns: {file_patterns}")
        
        try:
            # For each file pattern, find matching files and select them
            for pattern in file_patterns:
                self.logger.info(f"Selecting files matching pattern: {pattern}")
                checkbox = utils.expect_by_XPATH(
                    self.driver,
                    f"//td[contains(text(), '{pattern}')]/preceding-sibling::td/input[@type='checkbox']"
                )
                checkbox.click()
            
            # Click the delete button
            delete_button = utils.expect_by_id(self.driver, "deleteButton")
            delete_button.click()
            
            # Confirm deletion
            confirm_button = utils.expect_by_id(self.driver, "confirmDeleteButton")
            confirm_button.click()
            
            # Handle any alert that might appear
            utils.handle_alert(self.driver)
            
            self.logger.info("Files deleted successfully")
        except TimeoutException as e:
            self.logger.error(f"Timeout while deleting files: {e}")
            raise
        except NoSuchElementException as e:
            self.logger.error(f"Element not found while deleting files: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error deleting files: {e}")
            raise
    
    def bulk_upload_files(self, file_paths):
        """
        Upload multiple files to VAN.
        
        Args:
            file_paths (list): A list of paths to the files to upload.
        
        Raises:
            TimeoutException: If elements cannot be found.
            NoSuchElementException: If elements cannot be found.
        """
        self.logger.info(f"Uploading {len(file_paths)} files")
        
        try:
            # Click the upload button
            upload_button = utils.expect_by_id(self.driver, "uploadButton")
            upload_button.click()
            
            # Find the file input element and send the file paths
            file_input = utils.expect_by_id(self.driver, "fileInput")
            
            # Join the file paths with the appropriate separator for the OS
            # For Windows, this is typically a newline character
            file_paths_str = '\n'.join(file_paths)
            file_input.send_keys(file_paths_str)
            
            # Click the submit button
            submit_button = utils.expect_by_id(self.driver, "submitUploadButton")
            submit_button.click()
            
            self.logger.info("Files uploaded successfully")
        except TimeoutException as e:
            self.logger.error(f"Timeout while uploading files: {e}")
            raise
        except NoSuchElementException as e:
            self.logger.error(f"Element not found while uploading files: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error uploading files: {e}")
            raise
    
    def verify_upload_success(self):
        """
        Verify that the file upload was successful.
        
        Returns:
            bool: True if the upload was successful, False otherwise.
        """
        self.logger.info("Verifying upload success")
        
        try:
            # Look for a success message
            utils.expect_by_XPATH(
                self.driver,
                "//div[contains(text(), 'Upload completed successfully')]"
            )
            self.logger.info("Upload verified as successful")
            return True
        except TimeoutException:
            self.logger.warning("Could not verify upload success")
            return False
        except Exception as e:
            self.logger.error(f"Error verifying upload success: {e}")
            return False