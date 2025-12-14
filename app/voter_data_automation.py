import logging
import json
import os
import utils
from voter_data_downloader import VoterDataDownloader
from van_file_manager import VANFileManager
from van_search_list_manager import VANSearchListManager

class VoterDataAutomation:
    """
    Main orchestration class for the VoterData automation process.
    
    This class coordinates the entire process of downloading VoterData files,
    managing them in VAN, and processing searches and lists.
    """
    
    def __init__(self, config_path="voter_data_config.json"):
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
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config["files"]["log_file"]),
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
    
    def initialize(self):
        """
        Initialize the automation components.
        
        This method starts the WebDriver, initializes the downloader, file manager,
        and search list manager, and navigates to the VoteBuilder website.
        
        Raises:
            Exception: If initialization fails.
        """
        self.logger.info("Initializing automation components")
        
        try:
            # Start the WebDriver
            self.driver = utils.start_driver()
            
            # Set implicit wait from config
            self.driver.implicitly_wait(self.config["selenium"]["implicit_wait"])
            
            # Navigate to the VoteBuilder website
            utils.get_page(self.driver, self.config["van"]["url"])
            
            # Login to VoteBuilder (user will complete 2FA)
            utils.login_to_page(self.driver)
            
            # Initialize the downloader
            self.downloader = VoterDataDownloader(
                base_url=self.config["api"]["base_url"],
                output_directory=self.config["files"]["output_directory"]
            )
            
            # Initialize the file manager
            self.file_manager = VANFileManager(self.driver)
            
            # Initialize the search list manager
            self.search_list_manager = VANSearchListManager(self.driver)
            
            self.logger.info("Automation components initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing automation components: {e}")
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
    
    def download_and_upload_files(self):
        """
        Download VoterData files and upload them to VAN.
        
        This method downloads the VoterData files from the API, deletes any existing
        files in the "VAT Lists (MT)" folder in VAN, and uploads the downloaded files.
        
        Raises:
            Exception: If download or upload fails.
        """
        self.logger.info("Starting download and upload process")
        
        try:
            # Get the file IDs
            file_ids = self.get_file_ids()
            
            # Download all files
            self.logger.info(f"Downloading {len(file_ids)} files")
            downloaded_files = self.downloader.download_all_files(file_ids)
            self.logger.info(f"Successfully downloaded {len(downloaded_files)} files")
            
            # Navigate to the list folder specified in config
            list_folder = self.config["van"]["folders"]["list_folder"]
            self.logger.info(f"Navigating to {list_folder} folder")
            self.file_manager.navigate_to_file_folder(list_folder)
            
            # Delete existing files
            self.logger.info("Deleting existing files")
            self.file_manager.delete_files([f"{file_id}_VoterData" for file_id in file_ids])
            
            # Upload the downloaded files
            self.logger.info("Uploading files")
            self.file_manager.bulk_upload_files(downloaded_files)
            
            # Verify upload success
            if self.file_manager.verify_upload_success():
                self.logger.info("Upload verified as successful")
            else:
                self.logger.warning("Could not verify upload success")
        except Exception as e:
            self.logger.error(f"Error in download and upload process: {e}")
            raise
    
    def process_searches_and_lists(self):
        """
        Process searches and lists in VAN.
        
        This method loads each search in the "VAT Searches" folder, saves the resulting
        list in the "VAT Lists (MT)" folder, and then loads and saves each list in the
        "VAT Lists (MT)" folder to replace the bulk uploaded version.
        
        Raises:
            Exception: If processing fails.
        """
        self.logger.info("Starting search and list processing")
        
        try:
            # Get folder names from config
            search_folder = self.config["van"]["folders"]["search_folder"]
            list_folder = self.config["van"]["folders"]["list_folder"]
            
            # Process all searches
            self.logger.info(f"Processing all searches in {search_folder}")
            self.search_list_manager.process_all_searches(search_folder, list_folder)
            
            # Process all lists
            self.logger.info(f"Processing all lists in {list_folder}")
            self.search_list_manager.process_all_lists(list_folder)
            
            self.logger.info("Search and list processing completed successfully")
        except Exception as e:
            self.logger.error(f"Error in search and list processing: {e}")
            raise
    
    def run_full_process(self):
        """
        Run the full automation process.
        
        This method coordinates the entire process of downloading VoterData files,
        managing them in VAN, and processing searches and lists.
        
        Raises:
            Exception: If any part of the process fails.
        """
        self.logger.info("Starting full automation process")
        
        try:
            # Initialize components
            self.initialize()
            
            # Download and upload files
            self.download_and_upload_files()
            
            # Process searches and lists
            self.process_searches_and_lists()
            
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