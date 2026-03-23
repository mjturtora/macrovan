# 1. Standard Library
import logging
import time
from datetime import datetime
from pathlib import Path
import sys

# 2. Third-Party Libraries
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# 3. Local Application Imports
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
        # Use the logger configured by the orchestrator
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
    
    def delete_files(self, file_patterns, folder_name):
        """
        Delete files in VAN that match the specified patterns.
        
        Uses the filter field to search for each file individually, then deletes them
        one at a time. Skips files that don't exist (prevents timeout issues).
        
        Args:
            file_patterns (list): A list of file name patterns to match for deletion.
            folder_name (str): The name of the folder being operated on.
            
        Returns:
            int: The number of files successfully deleted.
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
                filter_xpath = f"//input[@id='{filter_selector.split('#')[1]}']"
                filter_field = utils.expect_by_XPATH(self.driver, filter_xpath)
                filter_field.send_keys(filename)
                filter_field.send_keys("\n")  # Submit the filter
                
                # Wait briefly for filter to apply
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
                    utils.get_page(self.driver, url='https://www.votebuilder.com/Default.aspx')
                    self.logger.info(f"Navigating to folder: {folder_name}")
                    self.navigate_to_file_folder(folder_name)
                    continue

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

        # sleep a long time to ensure the files are fully deleted
        time.sleep(2) 
        self.logger.info(f"Deletion complete: {deleted_count} deleted, {skipped_count} skipped")
        
        # RETURN RECEIPT for the orchestrator
        return deleted_count


    def bulk_upload_files(self, file_paths, list_folder):
        """
        Uploads local files into the VAN system with a bulletproof 3-attempt retry loop.
        
        Args:
            file_paths (list): A list of local file paths to upload.
            list_folder (str): The destination folder name in VAN.
            
        Returns:
            int: The total count of successfully uploaded files.
        """
        uploaded_count = 0
        failed_files = []

        for file_path in file_paths:
            path_obj = Path(file_path).resolve()
            filename = path_obj.stem

            self.logger.info(f"\n--- Processing: {filename} ---")
            
            success = False
            for attempt in range(3):
                try:
                    self.logger.info(f"1. Uploading file (Attempt {attempt + 1}/3)...")
                    self.driver.get("https://www.votebuilder.com/UploadDataSelectType.aspx")
                    
                    if attempt == 0:
                        self.driver.refresh()

                    utils.click_button(self.driver, "//option[. = 'State File ID']", "Select State File ID", locator_type=By.XPATH)
                    utils.click_button(self.driver, "ctl00_ContentPlaceHolderVANPage_ButtonUploadSubmit", "Upload Submit", locator_type=By.ID)
                    
                    file_input = utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_InputFileDefault")
                    file_input.send_keys(str(path_obj))
                    time.sleep(4) # Solid Attachment pause
                    
                    utils.click_button(self.driver, "ctl00_ContentPlaceHolderVANPage_ButtonSubmitDefault", "Process File", locator_type=By.ID)

                    # 2. SMART WAIT: Poll for response (OOPS vs Success)
                    response_found = False
                    for _ in range(22): # ~22 seconds max
                        time.sleep(1)
                        if "Error.aspx" in self.driver.current_url:
                            error_msg = "Unknown Error"
                            try:
                                error_msg = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolderVANPage_LabelErrorText").text
                            except:
                                pass
                            # Manually trigger the except block to force a retry
                            raise Exception(f"VAN Error.aspx encountered: {error_msg}")
                        
                        if len(self.driver.find_elements(By.NAME, "ctl00$ContentPlaceHolderVANPage$ctl09")) > 0:
                            response_found = True
                            break

                    if not response_found:
                        raise Exception("Timeout waiting for 'Unmatched People' button to appear.")

                    # Step 2: Unmatched Alert
                    self.logger.info(f"2. Waiting for Unmatched People...")
                    utils.click_button(self.driver, 'ctl00$ContentPlaceHolderVANPage$ctl09', "Unmatched Button", locator_type=By.NAME)
                    
                    # Step 3: Trigger Save-as-List Overlay
                    self.logger.info("3. Waiting for Mapping Dropdown...")
                    time.sleep(1)
                    dropdown_element = utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_ctl03_AddULFieldID")
                    Select(dropdown_element).select_by_value("154")

                    # Step 4: Fill Overlay (Iframe Context)
                    self.logger.info("4. Waiting for Overlay...")
                    self.driver.switch_to.frame(self.driver.find_element(By.NAME, "RadWindow1"))
                    
                    name_field = utils.expect_by_id(self.driver, "ctl01_ContentPlaceHolderVANPage_myLabelCont0_ListName_ListName_tb_ListName")
                    name_field.send_keys(filename)
                    
                    folder_drop_element = utils.expect_by_id(self.driver, "ctl01_ContentPlaceHolderVANPage_myLabelCont0_FolderID_FolderID_ddl_FolderID")
                    Select(folder_drop_element).select_by_visible_text(list_folder)

                    # Step 5: Click Next and Exit Iframe
                    self.logger.info("5. Clicking Next and Exiting Iframe...")
                    utils.click_button(self.driver, "ctl01_ContentPlaceHolderVANPage_Next0", "Overlay Next", locator_type=By.ID)
                    
                    time.sleep(5) 
                    self.driver.switch_to.default_content()
                    
                    # Step 6: Final Finish
                    self.logger.info("6. Waiting for First Finish...")
                    utils.click_button(self.driver, "ctl00_ContentPlaceHolderVANPage_ButtonFinishUpload", "Finish 1", locator_type=By.ID)
                    utils.click_button(self.driver, "ctl00_ContentPlaceHolderVANPage_FinishUploadModal__submitButton", "Finish 2", locator_type=By.ID)
                    
                    # IF WE REACH THIS LINE, ALL 6 STEPS PASSED
                    self.logger.info(f"Success: {filename}")
                    success = True
                    break 

                except Exception as e:
                    # Catch ANY failure in steps 1-6, log it, and loop back for the next attempt
                    self.logger.warning(f"Upload attempt {attempt + 1} failed for {filename}: {e}")
                    time.sleep(3) # Short breather before retrying
                    continue

            if success:
                uploaded_count += 1
            else:
                self.logger.error(f"FATAL: Could not upload {filename} after all retries.")
                failed_files.append(filename)

            time.sleep(5)
            
        if failed_files:
            self.logger.error(f"Bulk upload finished with {len(failed_files)} failures: {failed_files}")

        return uploaded_count


    def verify_upload_success(self, file_ids, timeout_minutes=5):
        """Poll Batches List until all target files show as 100% Processed."""
        now = datetime.now()
        today_str = f"{now.month}/{now.day}/{now.strftime('%y')}"
        
        target_filenames = [f"{fid}_VoterData" for fid in file_ids]
        self.logger.info(f"Verifying {len(target_filenames)} files. Max wait: {timeout_minutes} mins.")
        
        try:
            if "BulkUploadBatchesList.aspx" not in self.driver.current_url:
                self.driver.get("https://www.votebuilder.com/BulkUploadBatchesList.aspx")

            end_time = time.time() + (timeout_minutes * 60)
            table_xpath = "//table[contains(., 'Import Name')]"
            
            while time.time() < end_time:
                utils.expect_by_XPATH(self.driver, table_xpath)
                rows = self.driver.find_elements(By.XPATH, f"{table_xpath}//tr")
                
                status_dict = {target: "Not Found" for target in target_filenames}
                
                for target in target_filenames:
                    for row in rows:
                        row_text = row.text
                        if target in row_text:
                            if today_str not in row_text:
                                status_dict[target] = "Old Date"
                            elif "100% Processed" in row_text:
                                status_dict[target] = "Complete"
                            elif any(x in row_text for x in ["Created", "Processing", "%"]):
                                status_dict[target] = "Processing"
                            else:
                                status_dict[target] = f"Unknown: {row_text[:20]}..."
                            break 

                self.logger.info(f"Poll result: {status_dict}")

                # Success: Every single file is marked complete
                if all(s == "Complete" for s in status_dict.values()):
                    self.logger.info("All files successfully verified as 100% Processed.")
                    return True
                
                # BUG FIX: If ANY file is not complete (Processing, Not Found, Old Date), keep waiting!
                if any(s != "Complete" for s in status_dict.values()):
                    self.logger.info("Files still processing or not yet visible. Waiting 15s...")
                    time.sleep(15)
                    self.driver.refresh()
                    continue

            self.logger.error(f"Verification timed out after {timeout_minutes} minutes.")
            return False

        except Exception as e:
            self.logger.error(f"Verification logic crashed: {e}")
            return False