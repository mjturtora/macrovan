import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import utils

class VANSearchListManager:
    """
    A class for managing searches and lists in the VAN interface.
    
    This class handles operations related to searches and lists in VAN, including
    navigating to search folders, loading searches, saving lists, and processing
    multiple searches and lists.
    """
    
    def __init__(self, driver):
        """
        Initialize the VANSearchListManager.
        
        Args:
            driver: The Selenium WebDriver instance to use for browser automation.
        """
        self.driver = driver
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('VANSearchListManager')
    
    def navigate_to_search_folder(self, folder_name):
        """
        Navigate to a specific search folder in VAN.
        
        Args:
            folder_name (str): The name of the folder to navigate to.
        
        Raises:
            TimeoutException: If the folder element cannot be found.
        """
        self.logger.info(f"Navigating to search folder: {folder_name}")
        
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
    
    def load_search(self, search_name):
        """
        Load a saved search in VAN.
        
        Args:
            search_name (str): The name of the search to load.
        
        Raises:
            TimeoutException: If elements cannot be found.
            NoSuchElementException: If elements cannot be found.
        """
        self.logger.info(f"Loading search: {search_name}")
        
        try:
            # Enter the search name in the search box
            search_input = utils.expect_by_id(self.driver, "searchNameInput")
            search_input.send_keys(search_name)
            
            # Click the search button
            search_button = utils.expect_by_id(self.driver, "searchButton")
            search_button.click()
            
            # Click on the search result
            search_result = utils.expect_by_XPATH(
                self.driver,
                f"//a[contains(text(), '{search_name}')]"
            )
            search_result.click()
            
            # Handle any alert that might appear (e.g., "overwrite current list")
            utils.handle_alert(self.driver)
            
            self.logger.info(f"Successfully loaded search: {search_name}")
        except TimeoutException as e:
            self.logger.error(f"Timeout while loading search {search_name}: {e}")
            raise
        except NoSuchElementException as e:
            self.logger.error(f"Element not found while loading search {search_name}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading search {search_name}: {e}")
            raise
    
    def save_list(self, list_name, folder_name, replace_existing=False):
        """
        Save the current list in VAN.
        
        Args:
            list_name (str): The name to save the list as.
            folder_name (str): The folder to save the list in.
            replace_existing (bool): Whether to replace an existing list with the same name.
        
        Raises:
            TimeoutException: If elements cannot be found.
            NoSuchElementException: If elements cannot be found.
        """
        self.logger.info(f"Saving list as: {list_name} in folder: {folder_name}")
        
        try:
            # Click the save list button
            save_button = utils.expect_by_id(self.driver, "saveListButton")
            save_button.click()
            
            # Enter the list name
            list_name_input = utils.expect_by_id(self.driver, "listNameInput")
            list_name_input.clear()
            list_name_input.send_keys(list_name)
            
            # Select the folder
            folder_dropdown = utils.expect_by_id(self.driver, "folderDropdown")
            folder_dropdown.click()
            folder_option = utils.expect_by_XPATH(
                self.driver,
                f"//option[contains(text(), '{folder_name}')]"
            )
            folder_option.click()
            
            # Check the replace existing checkbox if needed
            if replace_existing:
                replace_checkbox = utils.expect_by_id(self.driver, "replaceExistingCheckbox")
                replace_checkbox.click()
            
            # Click the submit button
            submit_button = utils.expect_by_id(self.driver, "submitSaveButton")
            submit_button.click()
            
            self.logger.info(f"Successfully saved list: {list_name}")
        except TimeoutException as e:
            self.logger.error(f"Timeout while saving list {list_name}: {e}")
            raise
        except NoSuchElementException as e:
            self.logger.error(f"Element not found while saving list {list_name}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error saving list {list_name}: {e}")
            raise
    
    def load_list(self, list_name, folder_name):
        """
        Load a saved list in VAN.
        
        Args:
            list_name (str): The name of the list to load.
            folder_name (str): The folder containing the list.
        
        Raises:
            TimeoutException: If elements cannot be found.
            NoSuchElementException: If elements cannot be found.
        """
        self.logger.info(f"Loading list: {list_name} from folder: {folder_name}")
        
        try:
            # Click on the list link
            list_link = utils.expect_by_XPATH(
                self.driver,
                f"//a[contains(text(), '{list_name}')]"
            )
            list_link.click()
            
            # Handle any alert that might appear (e.g., "overwrite current list")
            utils.handle_alert(self.driver)
            
            self.logger.info(f"Successfully loaded list: {list_name}")
        except TimeoutException as e:
            self.logger.error(f"Timeout while loading list {list_name}: {e}")
            raise
        except NoSuchElementException as e:
            self.logger.error(f"Element not found while loading list {list_name}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading list {list_name}: {e}")
            raise
    
    def get_search_names(self):
        """
        Get the names of all searches in the current folder.
        
        Returns:
            list: A list of search names.
        
        Raises:
            TimeoutException: If elements cannot be found.
        """
        self.logger.info("Getting search names from current folder")
        
        try:
            # Find all search links
            search_elements = utils.expect_by_XPATH(
                self.driver,
                "//a[contains(@class, 'searchName')]"
            )
            
            # Extract the text from each element
            search_names = [element.text for element in search_elements]
            
            self.logger.info(f"Found {len(search_names)} searches")
            return search_names
        except TimeoutException as e:
            self.logger.error(f"Timeout while getting search names: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error getting search names: {e}")
            raise
    
    def get_list_names(self):
        """
        Get the names of all lists in the current folder.
        
        Returns:
            list: A list of list names.
        
        Raises:
            TimeoutException: If elements cannot be found.
        """
        self.logger.info("Getting list names from current folder")
        
        try:
            # Find all list links
            list_elements = utils.expect_by_XPATH(
                self.driver,
                "//a[contains(@class, 'listName')]"
            )
            
            # Extract the text from each element
            list_names = [element.text for element in list_elements]
            
            self.logger.info(f"Found {len(list_names)} lists")
            return list_names
        except TimeoutException as e:
            self.logger.error(f"Timeout while getting list names: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error getting list names: {e}")
            raise
    
    def process_all_searches(self, search_folder, list_folder):
        """
        Process all searches in a folder, saving each as a list.
        
        Args:
            search_folder (str): The folder containing the searches.
            list_folder (str): The folder to save the lists in.
        
        Raises:
            Exception: If any operation fails.
        """
        self.logger.info(f"Processing all searches in folder: {search_folder}")
        
        try:
            # Navigate to the search folder
            self.navigate_to_search_folder(search_folder)
            
            # Get all search names
            search_names = self.get_search_names()
            
            # Process each search
            for search_name in search_names:
                try:
                    self.logger.info(f"Processing search: {search_name}")
                    
                    # Load the search
                    self.load_search(search_name)
                    
                    # Save as a list with the same name
                    self.save_list(search_name, list_folder, replace_existing=True)
                    
                    self.logger.info(f"Successfully processed search: {search_name}")
                except Exception as e:
                    self.logger.error(f"Error processing search {search_name}: {e}")
                    raise
            
            self.logger.info(f"Successfully processed all {len(search_names)} searches")
        except Exception as e:
            self.logger.error(f"Error processing searches: {e}")
            raise
    
    def process_all_lists(self, list_folder):
        """
        Process all lists in a folder, loading and saving each one.
        
        Args:
            list_folder (str): The folder containing the lists.
        
        Raises:
            Exception: If any operation fails.
        """
        self.logger.info(f"Processing all lists in folder: {list_folder}")
        
        try:
            # Navigate to the list folder
            self.navigate_to_search_folder(list_folder)
            
            # Get all list names
            list_names = self.get_list_names()
            
            # Process each list
            for list_name in list_names:
                try:
                    self.logger.info(f"Processing list: {list_name}")
                    
                    # Load the list
                    self.load_list(list_name, list_folder)
                    
                    # Save the list again (to replace the bulk uploaded version)
                    self.save_list(list_name, list_folder, replace_existing=True)
                    
                    self.logger.info(f"Successfully processed list: {list_name}")
                except Exception as e:
                    self.logger.error(f"Error processing list {list_name}: {e}")
                    raise
            
            self.logger.info(f"Successfully processed all {len(list_names)} lists")
        except Exception as e:
            self.logger.error(f"Error processing lists: {e}")
            raise