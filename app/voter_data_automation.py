# 1. Standard Library
import logging
import sys
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
    Executes a 6-phase pipeline to synchronize external data with VAN.
    """

    def __init__(self, config_path="macrovan_config.json", file_override=None):
        # 1. Anchor to script location (EXE-aware)
        if getattr(sys, 'frozen', False):
            self.base_dir = Path(sys.executable).resolve().parent
        else:
            self.base_dir = Path(__file__).resolve().parent.parent

        # 2. Load config (Smart anchor: handles absolute or relative paths)
        path_obj = Path(config_path)
        if path_obj.is_absolute():
            self.config = load_config(path_obj)
        else:
            self.config = load_config(self.base_dir / path_obj)

        # 3. Standardize ONLY local file system paths to absolute
        self._resolve_config_paths()

        # 4. Core components
        self.driver = None
        self.file_manager = None
        self.file_override = file_override # Stores CLI subset if provided
        
        # Initialize downloader once with resolved paths
        self.downloader = VoterDataDownloader(
            base_url=self.config["api"]["base_url"],
            output_directory=self.config["files"]["output_directory"]
        )

        # Performance & Tracking Stats for final summary
        self.stats = {
            "files_downloaded": 0,
            "files_deleted": 0,
            "files_uploaded": 0,
            "searches_refreshed": 0,
            "lists_refreshed": 0
        }

        # 5. Configure logging (Explicitly anchored via resolved config)
        log_dir = Path(self.config["files"]["logs_directory"])
        log_file = self.config["files"]["log_files"]["vat_automation"]
        log_path = log_dir / log_file
        
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
                    rel_path = self.config["files"][key]
                    # Anchor the JSON path to our base_dir
                    self.config["files"][key] = str((self.base_dir / rel_path).resolve())


    def download_files_from_api(self):
        """
        Phase 1: Download VoterData files from API.
        """
        self.logger.info("Phase 1: Downloading files from API")
        
        try:
            # Downloader is already initialized in __init__
            file_ids = self.get_file_ids()
            self.downloaded_files = self.downloader.download_all_files(file_ids)
            
            self.stats["files_downloaded"] = len(self.downloaded_files)
            self.logger.info(f"Successfully downloaded/verified {len(self.downloaded_files)} files")
        except Exception as e:
            self.logger.error(f"Error downloading files from API: {e}")
            raise


    def initialize_browser(self):
        """
        Phase 2: Initialize browser and login to VAN.
        """
        self.logger.info("Phase 2: Initializing browser and logging in")
        
        try:
            self.driver = utils.start_driver(base_path=self.base_dir)

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
        """Get file IDs from config or override."""
        # Priority 1: CLI Argument (-f G10 G11)
        if self.file_override:
            return self.file_override
            
        # Priority 2: Manual Subsetter (Uncomment to use)
        # return ["G10", "G11"]
        
        # Priority 3: Default JSON Config
        return self.config["api"]["file_ids"]


    def upload_files_to_van(self):
        """
        Phase 3: Cleanup existing files in VAN.
        Phase 4: Upload previously downloaded files to VAN.
        Includes "Halt and Catch Fire" logic to prevent stale data refreshes.
        """
        list_folder = self.config["van"]["folders"]["list_folder"]
        file_ids = self.get_file_ids()
        
        try:
            # --- PHASE 3: CLEANUP ---
            self.logger.info("Phase 3: Cleanup existing files in VAN")
            self.file_manager.navigate_to_file_folder(list_folder)
            
            self.logger.info(f"Phase 3: Deleting {len(file_ids)} existing files")
            self.stats["files_deleted"] = self.file_manager.delete_files(
                [f"{file_id}_VoterData" for file_id in file_ids], 
                list_folder
            )
            
            # --- PHASE 4: IMPORT & VERIFY ---
            self.logger.info("Phase 4: Uploading new files to VAN")
            uploaded_count, alerts = self.file_manager.bulk_upload_files(self.downloaded_files, list_folder)
            self.stats["files_uploaded"] = uploaded_count
            self.stats["alerts"] = alerts

            # HALT AND CATCH FIRE 1: Count Mismatch
            if self.stats["files_uploaded"] < len(self.downloaded_files):
                error_msg = "\n" + "!"*65 + "\n!!! CRITICAL FAILURE: NOT ALL FILES WERE SUCCESSFULLY UPLOADED !!!\n" + "!"*65
                self.logger.error(error_msg)
                raise RuntimeError("Upload count mismatch. Halting pipeline to prevent stale data refresh.")

            # HALT AND CATCH FIRE 2: Verification Timeout
            if self.file_manager.verify_upload_success(file_ids):
                self.logger.info("Phase 4: Upload verified as successful")
            else:
                error_msg = "\n" + "!"*65 + "\n!!! CRITICAL FAILURE: VAN UPLOAD VERIFICATION TIMED OUT !!!\n" + "!"*65
                self.logger.error(error_msg)
                raise RuntimeError("VAN processing timeout. Halting pipeline to prevent stale data refresh.")

        except Exception as e:
            self.logger.error(f"Error during VAN file upload/cleanup: {e}")
            raise

    def refresh_searches(self):
        """
        Phase 5: Loads saved searches and overwrites existing lists.
        """
        search_folder = self.config["van"]["folders"]["search_folder"]
        list_folder = self.config["van"]["folders"]["list_folder"]
        file_ids = self.get_file_ids()
        
        suffixes = ["_BadAddress", "_LL_NPA"]
        self.logger.info(f"Starting Phase 5: Processing searches in {search_folder}")

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
                    
                    self.stats["searches_refreshed"] += 1

                except Exception as e: 
                    self.logger.error(f"Failed to process {target_name}: {e}")
                    continue
        self.logger.info("Phase 5 complete.")

    def refresh_lists(self):
        """
        Phase 6: Refreshes VoterData lists to force a data update.
        """
        list_folder = self.config["van"]["folders"]["list_folder"]
        file_ids = self.get_file_ids()
        suffixes = ["_VoterData"]
        
        self.logger.info(f"Starting Phase 6: Refreshing lists in {list_folder}")

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
                    
                    self.stats["lists_refreshed"] += 1

                except Exception as e:
                    self.logger.error(f"Failed to refresh list {target_name}: {e}")
                    continue
        self.logger.info("Phase 6 complete.")

    def run_full_process(self):
        """Orchestrates the 6-phase pipeline."""
        self.logger.info("Starting full 6-phase automation process")
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


    def cleanup(self):
        """Clean up WebDriver resources safely."""
        if self.driver:
            self.logger.info("Cleaning up resources")
            try:
                self.driver.quit()
                self.logger.info("WebDriver quit successfully")
            except Exception as e:
                self.logger.debug(f"WebDriver was already closed or unreachable: {e}")
            finally:
                # CRITICAL: Set to None so a second call does nothing
                self.driver = None