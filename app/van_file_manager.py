import os
import logging
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            # First click on "View my folders" link
            self.logger.info("Clicking on 'View my folders' link")
            view_folders_link = utils.expect_by_XPATH(
                self.driver,
                "//*[@id='ctl00_ContentPlaceHolderVANPage_HyperLinkMenuSavedLists']"
            )
            view_folders_link.click()
            self.logger.info("Successfully clicked on 'View my folders' link")
            
            # Now find and click the folder link using the span with the folder name
            self.logger.info(f"Looking for folder: {folder_name}")
            folder_element = utils.expect_by_XPATH(
                self.driver,
                f"//span[@class='grid-result no-break' and contains(text(), '{folder_name}')]"
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
        
        Uses the filter field to search for each file individually, then deletes them
        one at a time. Skips files that don't exist (prevents timeout issues).
        
        Args:
            file_patterns (list): A list of file name patterns to match for deletion.
        
        Raises:
            TimeoutException: If critical elements cannot be found.
        """
        self.logger.info(f"Deleting files matching patterns: {file_patterns}")
        
        # CSS selector for the filter input field
        filter_selector = "input#ctl00_ContentPlaceHolderVANPage_VanInputItemviiFilterName_VanInputItemviiFilterName"
        
        deleted_count = 0
        skipped_count = 0
        
        for filename in file_patterns:
            self.logger.info(f"Attempting to delete: {filename}")
            
            try:
                # Wait for and interact with the filter field
                # Convert CSS selector to XPath (input#id -> //input[@id='id'])
                filter_xpath = f"//input[@id='{filter_selector.split('#')[1]}']"
                filter_field = utils.expect_by_XPATH(self.driver, filter_xpath)
                filter_field.send_keys(filename)
                filter_field.send_keys("\n")  # Submit the filter
                
                # Wait briefly for filter to apply
                import time
                time.sleep(1)
                
                # Try to find the Edit button for this file (short timeout for existence check)
                edit_button_xpath = f"//tr[contains(., '{filename}')]//span[contains(text(), 'Edit')]"
                
                try:
                    # Use WebDriverWait directly with a short timeout (5 seconds)
                    edit_button = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, edit_button_xpath))
                    )
                    edit_button.click()
                    self.logger.info(f"Clicked Edit button for {filename}")
                except TimeoutException:
                    self.logger.warning(f"File {filename} not found - skipping")
                    skipped_count += 1
                    continue
                
                # Now we're on the detail page - click the delete button
                # Now we're on the detail page - click the delete button (use standard timeout)
                delete_button = utils.expect_by_XPATH(
                    self.driver,
                    "//input[@id='ctl00_ContentPlaceHolderVANPage_ButtonDeleteList']"
                )
                delete_button.click()
                
                # Wait for alert and accept it
                time.sleep(1.5)
                try:
                    self.driver.switch_to.alert.accept()
                    self.logger.info(f"Confirmed deletion for {filename}")
                except:
                    self.logger.warning(f"No alert appeared for {filename}")
                
                # Wait for return to the list view (filter field appears again)
                filter_xpath = f"//input[@id='{filter_selector.split('#')[1]}']"
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, filter_xpath))
                )
                
                deleted_count += 1
                self.logger.info(f"Successfully deleted {filename}")
                
            except Exception as e:
                self.logger.error(f"Error deleting {filename}: {e}")
                # Continue with next file instead of failing completely
                skipped_count += 1
                continue
        
        self.logger.info(f"Deletion complete: {deleted_count} deleted, {skipped_count} skipped")
    
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