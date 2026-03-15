# 1. Standard Library
import json
import logging
import os
import time
from pathlib import Path

# 2. Third-Party Libraries
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# 3. Local Application Imports
import utils
from utils import load_config
from van_file_manager import VANFileManager
from voter_data_downloader import VoterDataDownloader

class VoterDataAutomation:
    """
    Main orchestration class for the VoterData automation process.
    """

    def __init__(self, config_path="macrovan_config.json"):
        # 1. Anchor to script location
        self.script_dir = Path(__file__).resolve().parent
        
        # 2. Load config using centralized utility
        self.config = load_config(self.script_dir / config_path)
        
        # 3. Standardize ONLY local file system paths to absolute
        self._resolve_config_paths()

        # 4. Core components
        self.driver = None
        self.downloader = None
        self.file_manager = None
        
        # 5. Configure logging using resolved paths
        log_dir = self.config["files"]["logs_directory"]
        log_file = self.config["files"]["log_files"]["vat_automation"]
        log_path = Path(log_dir) / log_file
        
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(str(log_path)),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('VoterDataAutomation')


    def _resolve_config_paths(self):
        """Converts relative LOCAL paths in config to absolute paths."""

        if "files" in self.config:
            for key in ["logs_directory", "output_directory"]:
                if key in self.config["files"]:
                    rel = self.config["files"][key]
                    self.config["files"][key] = str((self.script_dir / rel).resolve())


    def download_files_from_api(self):
        """
        Download VoterData files from API.
        """
        self.logger.info("Phase 1: Downloading files from API")
        
        try:
            self.downloader = VoterDataDownloader(
                base_url=self.config["api"]["base_url"],
                output_directory=self.config["files"]["output_directory"]
            )
            
            file_ids = self.get_file_ids()
            self.downloaded_files = self.downloader.download_all_files(file_ids)
            
            self.logger.info(f"Successfully downloaded/verified {len(self.downloaded_files)} files")
        except Exception as e:
            self.logger.error(f"Error downloading files from API: {e}")
            raise
    
    def initialize_browser(self):
        """
        Initialize browser and login to VAN.
        """
        self.logger.info("Phase 2: Initializing browser and logging in")
        
        try:
            self.driver = utils.start_driver()
            self.driver.implicitly_wait(self.config["selenium"]["implicit_wait"])
            
            utils.get_page(self.driver, self.config["van"]["url"])
            utils.login_to_page(self.driver)
            
            self.file_manager = VANFileManager(self.driver)
            self.logger.info("Browser initialization and login completed successfully")
        except Exception as e:
            self.logger.error(f"Error initializing browser: {e}")
            if self.driver:
                self.driver.quit()
            raise
    
    def get_file_ids(self):
        """Get file IDs from config."""
        return self.config["api"]["file_ids"]
    
    def upload_files_to_van(self):
        """
        Upload previously downloaded files to VAN.
        """
        self.logger.info("Phase 3: Uploading files to VAN")
        
        try:
            list_folder = self.config["van"]["folders"]["list_folder"]
            file_ids = self.get_file_ids()
            
            self.file_manager.navigate_to_file_folder(list_folder)
            
            self.logger.info("Deleting existing files")
            self.file_manager.delete_files(
                [f"{file_id}_VoterData" for file_id in file_ids], 
                list_folder
            )
            
            self.logger.info("Uploading files")
            self.file_manager.bulk_upload_files(self.downloaded_files, list_folder)
            
            if self.file_manager.verify_upload_success(file_ids):
                self.logger.info("Upload verified as successful")
            else:
                self.logger.warning("Could not verify upload success")
        except Exception as e:
            self.logger.error(f"Error uploading files to VAN: {e}")
            raise

    def refresh_searches(self):
        """
        Phase 4: Loads saved searches and overwrites existing lists.
        """
        search_folder = self.config["van"]["folders"]["search_folder"]
        list_folder = self.config["van"]["folders"]["list_folder"]
        file_ids = self.get_file_ids()
        
        suffixes = ["_BadAddress", "_LL_NPA"]
        self.logger.info(f"Starting Phase 4: Processing searches in {search_folder}")

        filter_id = "ctl00_ContentPlaceHolderVANPage_VanInputItemviiFilterName_VanInputItemviiFilterName"
        save_as_id = "ctl00_ContentPlaceHolderVANPage_saveAsButton"
        
        for file_id in file_ids:
            for suffix in suffixes:
                target_name = f"{file_id}{suffix}"
                self.logger.info(f"Processing search: {target_name}")
                
                try:
                    utils.get_page(self.driver, url='https://www.votebuilder.com/Default.aspx')
                    self.file_manager.navigate_to_file_folder(search_folder)

                    filter_field = utils.expect_by_id(self.driver, filter_id)
                    filter_field.clear()
                    filter_field.send_keys(target_name)
                    filter_field.send_keys("\n")
                    
                    search_link_xpath = f"//span[contains(text(), '{target_name}')] | //a[contains(text(), '{target_name}')]"
                    utils.expect_clickable_by_XPATH(self.driver, search_link_xpath, wait_time=10).click()
                    
                    utils.expect_alert(self.driver, wait_time=5)
                    self.driver.switch_to.alert.accept()
                    
                    utils.expect_by_id(self.driver, save_as_id).click()
                    utils.expect_by_id(self.driver, "SaveListRadioBtn").click()
                    utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemNew_VANInputItemDetailsItemNew_New_1").click()
                    
                    Select(utils.expect_by_id(self.driver, "Folder")).select_by_visible_text(list_folder)
                    time.sleep(2)
                    
                    try:
                        replace_dropdown = Select(utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemReplace_VANInputItemDetailsItemReplace_Replace"))
                        replace_dropdown.select_by_visible_text(target_name)
                    except Exception:
                        self.logger.warning(f"List '{target_name}' not found. Creating as NEW.")
                        utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemNew_VANInputItemDetailsItemNew_New_0").click()
                        name_input = utils.expect_by_id(self.driver, "Name")
                        name_input.clear()
                        name_input.send_keys(target_name)

                    utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_SubmitButton").click()
                    utils.expect_by_id(self.driver, save_as_id)
                    self.logger.info(f"Successfully replaced list: {target_name}")

                except Exception as e: 
                    self.logger.error(f"Failed to process {target_name}: {e}")
                    continue
        self.logger.info("Phase 4 complete.")

    def refresh_lists(self):
        """
        Phase 5: Refreshes VoterData lists to force a data update.
        """
        list_folder = self.config["van"]["folders"]["list_folder"]
        file_ids = self.get_file_ids()
        suffixes = ["_VoterData"]
        
        self.logger.info(f"Starting Phase 5: Refreshing lists in {list_folder}")

        filter_id = "ctl00_ContentPlaceHolderVANPage_VanInputItemviiFilterName_VanInputItemviiFilterName"
        save_as_id = "ctl00_ContentPlaceHolderVANPage_saveAsButton"
        
        for file_id in file_ids:
            for suffix in suffixes:
                target_name = f"{file_id}{suffix}"
                self.logger.info(f"Refreshing data for list: {target_name}")
                
                try:
                    utils.get_page(self.driver, url='https://www.votebuilder.com/Default.aspx')
                    self.file_manager.navigate_to_file_folder(list_folder)

                    filter_field = utils.expect_by_id(self.driver, filter_id)
                    filter_field.clear()
                    filter_field.send_keys(target_name)
                    filter_field.send_keys("\n")
                    
                    list_link_xpath = f"//span[contains(text(), '{target_name}')] | //a[contains(text(), '{target_name}')]"
                    utils.expect_clickable_by_XPATH(self.driver, list_link_xpath, wait_time=10).click()
                    
                    utils.expect_alert(self.driver, wait_time=5)
                    self.driver.switch_to.alert.accept()
                    
                    utils.expect_by_id(self.driver, save_as_id).click()
                    utils.expect_by_id(self.driver, "SaveListRadioBtn").click()
                    utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_VanDetailsItemNew_VANInputItemDetailsItemNew_New_1").click()
                    
                    Select(utils.expect_by_id(self.driver, "Folder")).select_by_visible_text(list_folder)
                    time.sleep(2) 
                    
                    replace_id = "ctl00_ContentPlaceHolderVANPage_VanDetailsItemReplace_VANInputItemDetailsItemReplace_Replace"
                    Select(utils.expect_by_id(self.driver, replace_id)).select_by_visible_text(target_name)
                    
                    utils.expect_by_id(self.driver, "ctl00_ContentPlaceHolderVANPage_SubmitButton").click()
                    utils.expect_by_id(self.driver, save_as_id)
                    self.logger.info(f"Successfully refreshed: {target_name}")

                except Exception as e:
                    self.logger.error(f"Failed to refresh list {target_name}: {e}")
                    continue
        self.logger.info("Phase 5 complete.")

    def run_full_process(self):
        """Orchestrates the 5-phase pipeline."""
        self.logger.info("Starting full automation process")
        try:
            self.download_files_from_api()
            self.initialize_browser()
            self.upload_files_to_van()
            self.refresh_searches()
            self.refresh_lists()
            self.logger.info("Full automation process completed successfully.")
        except Exception as e:
            self.logger.error(f"Critical failure: {e}")
            raise
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up WebDriver resources."""
        self.logger.info("Cleaning up resources")
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver quit successfully")
            except Exception as e:
                self.logger.error(f"Error quitting WebDriver: {e}")

if __name__ == "__main__":
    automation = VoterDataAutomation()
    try:
        automation.run_full_process()
    except Exception as e:
        print(f"Error: {e}")