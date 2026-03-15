import logging
import json
import os
import time
import utils
from voter_data_downloader import VoterDataDownloader
from van_file_manager import VANFileManager
from van_search_list_manager import VANSearchListManager

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


class VoterDataAutomation:
    """
    Main orchestration class for the VoterData automation process.
    
    This class coordinates the entire process of downloading VoterData files,
    managing them in VAN, and processing searches and lists.
    """
    
    def __init__(self, config_path="macrovan_config.json"):
        """
        Initialize the VoterDataAutomation object.
        
        Args:
            config_path (str): Path to the configuration file.
        """
        # These will be initialized in the initialize method
        self.driver = None
        self.downloader = None
        self.file_manager = None
        self.search_list_manager = None
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Configure logging
        log_path = os.path.join(
            self.config["files"]["logs_directory"],
            self.config["files"]["log_files"]["vat_automation"]
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
        self.logger = logging.getLogger('VoterDataAutomation')
    
    def _load_config(self, config_path):
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
    
    def download_files_from_api(self):
        """
        Download VoterData files from API.
        This operation is independent of VAN/browser and runs first.
        
        Raises:
            Exception: If download fails.
        """
        self.logger.info("Phase 1: Downloading files from API")
        
        try:
            # Initialize downloader (doesn't need browser)
            self.downloader = VoterDataDownloader(
                base_url=self.config["api"]["base_url"],
                output_directory=self.config["files"]["output_directory"]
            )
            
            # Download all files
            file_ids = self.get_file_ids()
            self.downloaded_files = self.downloader.download_all_files(file_ids)
            
            self.logger.info(f"Successfully downloaded/verified {len(self.downloaded_files)} files")
        except Exception as e:
            self.logger.error(f"Error downloading files from API: {e}")
            raise
    
    def initialize_browser(self):
        """
        Initialize browser and login to VAN.
        Only called AFTER API downloads are complete.
        
        Raises:
            Exception: If browser initialization or login fails.
        """
        self.logger.info("Phase 2: Initializing browser and logging in")
        
        try:
            # Start the WebDriver
            self.driver = utils.start_driver()
            
            # Set implicit wait from config
            self.driver.implicitly_wait(self.config["selenium"]["implicit_wait"])
            
            # Navigate to the VoteBuilder website
            utils.get_page(self.driver, self.config["van"]["url"])
            
            # Login to VoteBuilder (user will complete 2FA)
            utils.login_to_page(self.driver)
            
            # Initialize the file manager and search list manager
            self.file_manager = VANFileManager(self.driver)
            self.search_list_manager = VANSearchListManager(self.driver)

            self.logger.info("Browser initialization and login completed successfully")
        except Exception as e:
            self.logger.error(f"Error initializing browser: {e}")
            # Clean up if initialization fails
            if self.driver:
                self.driver.quit()
            raise
    
    def get_file_ids(self):
        """
        Get the IDs of the VoterData files to download.
        
        Returns:
            list: A list of file IDs.
        """
        # Get file IDs from config
        return self.config["api"]["file_ids"]
    
    def upload_files_to_van(self):
        """
        Upload previously downloaded files to VAN.
        Requires browser to be initialized and downloaded_files to be available.
        
        Raises:
            Exception: If upload fails.
        """
        self.logger.info("Phase 3: Uploading files to VAN")
        
        try:
            # Get configuration
            list_folder = self.config["van"]["folders"]["list_folder"]
            file_ids = self.get_file_ids()
            
            # Navigate to the list folder
            self.logger.info(f"Navigating to {list_folder} folder")
            self.file_manager.navigate_to_file_folder(list_folder)
            
            # Delete existing files
            self.logger.info("Deleting existing files")
            self.file_manager.delete_files(
                [f"{file_id}_VoterData" for file_id in file_ids]
                , list_folder
                )
            
            # Upload the downloaded files
            self.logger.info("Uploading files")
            self.file_manager.bulk_upload_files(self.downloaded_files)
            
            # Verify upload success
            if self.file_manager.verify_upload_success(file_ids):
                self.logger.info("Upload verified as successful")
            else:
                self.logger.warning("Could not verify upload success")
        except Exception as e:
            self.logger.error(f"Error uploading files to VAN: {e}")
            raise


    def refresh_searches(self):
        """
        Loads saved searches and overwrites existing lists using dynamic waits.
        """
        # Read directly from config to match upload_files_to_van()
        search_folder = self.config["van"]["folders"]["search_folder"]
        list_folder = self.config["van"]["folders"]["list_folder"]
        file_ids = self.get_file_ids()
        
        suffixes = ["_BadAddress", "_LL_NPA"]
        self.logger.info(f"Starting Phase 4: Processing searches in {search_folder}")

        # Use the specific ID you captured in your recording
        filter_id = "ctl00_ContentPlaceHolderVANPage_VanInputItemviiFilterName_VanInputItemviiFilterName"
        
        for file_id in file_ids:
            for suffix in suffixes:
                target_name = f"{file_id}{suffix}"
                self.logger.info(f"Processing search: {target_name}")
                
                try:
                    utils.get_page(self.driver, url='https://www.votebuilder.com/Default.aspx')
                    self.file_manager.navigate_to_file_folder(search_folder)

                    # 1. Filter using ID
                    filter_field = utils.expect_by_id(self.driver, filter_id)
                    filter_field.clear()
                    filter_field.send_keys(target_name)
                    filter_field.send_keys("\n")
                    
                    # Wait 1: Keep XPATH for text-based link finding
                    search_link_xpath = f"//span[contains(text(), '{target_name}')] | //a[contains(text(), '{target_name}')]"
                    search_link = utils.expect_clickable_by_XPATH(self.driver, search_link_xpath, wait_time=10)
                    search_link.click()
                    
                    # Wait 2: Alert
                    utils.expect_alert(self.driver, wait_time=5)
                    self.driver.switch_to.alert.accept()
                    
                    # 3. My List -> Save List As using ID
                    save_as_id = "ctl00_ContentPlaceHolderVANPage_saveAsButton"
                    save_as_btn = utils.expect_by_id(self.driver, save_as_id)
                    save_as_btn.click()
                    # 4. Radios (Default to Replace)
                    utils.expect_by_id(self.driver, "SaveListRadioBtn").click()
                    utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemNew_VANInputItemDetailsItemNew_New_1").click()
                    
                    # 5. Select Folder
                    folder_dropdown = Select(utils.expect_by_id(self.driver, "Folder"))
                    folder_dropdown.select_by_visible_text(list_folder)
                    
                    # Wait for AJAX to populate Replace dropdown based on folder choice
                    time.sleep(2)
                    
                    # 6. Attempt Replace, Fallback to New
                    try:
                        replace_dropdown = Select(utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemReplace_VANInputItemDetailsItemReplace_Replace"))
                        replace_dropdown.select_by_visible_text(target_name)
                    except Exception:  # Catches NoSuchElementException if name isn't in dropdown
                        self.logger.warning(f"*** WARNING: List '{target_name}' not found. Creating as NEW list. ***")
                        
                        # Click "New List" radio button
                        utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemNew_VANInputItemDetailsItemNew_New_0").click()
                        
                        # Enter the list name
                        name_input = utils.expect_by_id(self.driver, "Name")
                        name_input.clear()
                        name_input.send_keys(target_name)

                    # 7. Save
                    utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_SubmitButton").click()
                        
                    # Wait for return to My List using ID
                    utils.expect_by_id(self.driver, save_as_id)
                    self.logger.info(f"Successfully replaced list: {target_name}")

                except Exception as e: 
                    self.logger.error(f"Failed to process {target_name}: {e}")
                    continue
        self.logger.info("Phase 4 complete.")


    def run_full_process(self):
        """
        Run the full automation process.
        
        This method coordinates the entire process following the architectural plan:
        1. Download files from API (no browser needed)
        2. Initialize browser and login
        3. Upload files to VAN
        4. Process searches and lists
        
        Raises:
            Exception: If any part of the process fails.
        """
        self.logger.info("Starting full automation process")
        
        try:
            # Phase 1: Download from API (no browser needed)
            self.download_files_from_api()
            
            # Phase 2: Initialize browser and login
            self.initialize_browser()
            
            # Phase 3: Upload files to VAN
            self.upload_files_to_van()

            # Phase 4: Process searches and lists
            search_folder = self.config["van"]["folders"]["search_folder"]
            list_folder = self.config["van"]["folders"]["list_folder"]
            self.refresh_searches()

            self.logger.info("Full automation process completed successfully")
        except Exception as e:
            self.logger.error(f"Error in automation process: {e}")
            raise
        finally:
            # Clean up
            self.cleanup()
    
    def cleanup(self):
        """
        Clean up resources after automation.
        
        This method quits the WebDriver and performs any other necessary cleanup.
        """
        self.logger.info("Cleaning up resources")
        
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver quit successfully")
            except Exception as e:
                self.logger.error(f"Error quitting WebDriver: {e}")


if __name__ == "__main__":
    # Example usage
    automation = VoterDataAutomation()
    try:
        automation.run_full_process()
    except Exception as e:
        print(f"Error: {e}")
