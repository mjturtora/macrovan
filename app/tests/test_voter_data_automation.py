import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import will be available after we create the module
# from voter_data_automation import VoterDataAutomation

class TestVoterDataAutomation(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test."""
        # Import the module here to ensure it's reloaded for each test
        from voter_data_automation import VoterDataAutomation
        
        # Create the automation object
        self.automation = VoterDataAutomation()
        
        # Create mock objects for dependencies
        self.mock_downloader = MagicMock()
        self.mock_file_manager = MagicMock()
        self.mock_search_list_manager = MagicMock()
        self.mock_driver = MagicMock()
        
        # Inject mock dependencies
        self.automation.downloader = self.mock_downloader
        self.automation.file_manager = self.mock_file_manager
        self.automation.search_list_manager = self.mock_search_list_manager
        self.automation.driver = self.mock_driver
    
    @patch('utils.start_driver')
    @patch('utils.get_page')
    @patch('utils.login_to_page')
    @patch('voter_data_downloader.VoterDataDownloader')
    @patch('van_file_manager.VANFileManager')
    @patch('van_search_list_manager.VANSearchListManager')
    def test_initialize(self, mock_search_list_manager_class, mock_file_manager_class, 
                        mock_downloader_class, mock_login, mock_get_page, mock_start_driver):
        """Test initialization of the automation object."""
        # Setup mock returns
        mock_start_driver.return_value = self.mock_driver
        mock_downloader_class.return_value = self.mock_downloader
        mock_file_manager_class.return_value = self.mock_file_manager
        mock_search_list_manager_class.return_value = self.mock_search_list_manager
        
        # Reset the automation object to test initialization
        from voter_data_automation import VoterDataAutomation
        self.automation = VoterDataAutomation()
        
        # Call the method
        self.automation.initialize()
        
        # Assertions
        mock_start_driver.assert_called_once()
        mock_get_page.assert_called_once_with(self.mock_driver)
        mock_login.assert_called_once_with(self.mock_driver)
        mock_downloader_class.assert_called_once()
        mock_file_manager_class.assert_called_once_with(self.mock_driver)
        mock_search_list_manager_class.assert_called_once_with(self.mock_driver)
        self.assertEqual(self.automation.driver, self.mock_driver)
    
    def test_get_file_ids(self):
        """Test getting file IDs."""
        # Call the method
        result = self.automation.get_file_ids()
        
        # Assertions
        self.assertEqual(len(result), 10)
        self.assertIn("G01", result)
        self.assertIn("G10", result)
    
    def test_download_and_upload_files(self):
        """Test downloading and uploading files."""
        # Setup test data
        file_ids = ["G01", "G02", "G03"]
        downloaded_files = ["path/to/G01.csv", "path/to/G02.csv", "path/to/G03.csv"]
        
        # Setup mock returns
        self.mock_downloader.download_all_files.return_value = downloaded_files
        self.mock_file_manager.verify_upload_success.return_value = True
        
        # Mock the get_file_ids method
        with patch.object(self.automation, 'get_file_ids', return_value=file_ids):
            # Call the method
            self.automation.download_and_upload_files()
        
        # Assertions
        self.mock_downloader.download_all_files.assert_called_once_with(file_ids)
        self.mock_file_manager.navigate_to_file_folder.assert_called_with("VAT Lists (MT)")
        self.mock_file_manager.delete_files.assert_called_once()
        self.mock_file_manager.bulk_upload_files.assert_called_once_with(downloaded_files)
        self.mock_file_manager.verify_upload_success.assert_called_once()
    
    def test_process_searches_and_lists(self):
        """Test processing searches and lists."""
        # Call the method
        self.automation.process_searches_and_lists()
        
        # Assertions
        self.mock_search_list_manager.process_all_searches.assert_called_once_with(
            "VAT Searches", "VAT Lists (MT)"
        )
        self.mock_search_list_manager.process_all_lists.assert_called_once_with(
            "VAT Lists (MT)"
        )
    
    @patch.object(VoterDataAutomation, 'initialize')
    @patch.object(VoterDataAutomation, 'download_and_upload_files')
    @patch.object(VoterDataAutomation, 'process_searches_and_lists')
    @patch.object(VoterDataAutomation, 'cleanup')
    def test_run_full_process(self, mock_cleanup, mock_process, mock_download, mock_initialize):
        """Test running the full automation process."""
        # Call the method
        self.automation.run_full_process()
        
        # Assertions
        mock_initialize.assert_called_once()
        mock_download.assert_called_once()
        mock_process.assert_called_once()
        mock_cleanup.assert_called_once()
    
    def test_cleanup(self):
        """Test cleanup after automation."""
        # Call the method
        self.automation.cleanup()
        
        # Assertions
        self.mock_driver.quit.assert_called_once()


if __name__ == '__main__':
    unittest.main()