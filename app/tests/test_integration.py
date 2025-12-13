import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import sys

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voter_data_automation import VoterDataAutomation
from voter_data_downloader import VoterDataDownloader
from van_file_manager import VANFileManager
from van_search_list_manager import VANSearchListManager

class TestVoterDataIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a mock WebDriver
        self.mock_driver = MagicMock()
        
        # Create real instances with mock driver or test configuration
        self.downloader = VoterDataDownloader(
            base_url="https://vat.flddc.org/API/VoterData/", 
            output_directory=self.temp_dir
        )
        self.file_manager = VANFileManager(self.mock_driver)
        self.search_list_manager = VANSearchListManager(self.mock_driver)
        
        # Create the automation object with real dependencies but mock driver
        self.automation = VoterDataAutomation()
        self.automation.downloader = self.downloader
        self.automation.file_manager = self.file_manager
        self.automation.search_list_manager = self.search_list_manager
        self.automation.driver = self.mock_driver
    
    def tearDown(self):
        """Clean up after each test."""
        # Clean up temporary directory
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)
    
    @patch('requests.get')
    @patch.object(VANFileManager, 'navigate_to_file_folder')
    @patch.object(VANFileManager, 'delete_files')
    @patch.object(VANFileManager, 'bulk_upload_files')
    @patch.object(VANFileManager, 'verify_upload_success')
    def test_download_and_upload_integration(self, mock_verify, mock_upload, mock_delete, 
                                            mock_navigate, mock_requests_get):
        """Test the integration of downloading and uploading files."""
        # Setup mock responses for HTTP requests
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Test file content"
        mock_requests_get.return_value = mock_response
        
        # Setup mock returns for file manager
        mock_verify.return_value = True
        
        # Limit to just 2 files for the test
        file_ids = ["G01", "G02"]
        
        # Call the method that integrates downloading and uploading
        with patch.object(self.automation, 'get_file_ids', return_value=file_ids):
            # Only test the download and upload part
            self.automation.download_and_upload_files()
        
        # Assertions
        self.assertEqual(mock_requests_get.call_count, 2)
        mock_navigate.assert_called_once()
        mock_delete.assert_called_once()
        mock_upload.assert_called_once()
        
        # Verify files were created in temp directory
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "G01_VoterData.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "G02_VoterData.csv")))
    
    @patch.object(VANSearchListManager, 'navigate_to_search_folder')
    @patch.object(VANSearchListManager, 'get_search_names')
    @patch.object(VANSearchListManager, 'load_search')
    @patch.object(VANSearchListManager, 'save_list')
    @patch.object(VANSearchListManager, 'get_list_names')
    @patch.object(VANSearchListManager, 'load_list')
    def test_process_searches_and_lists_integration(self, mock_load_list, mock_get_list_names, 
                                                  mock_save_list, mock_load_search, 
                                                  mock_get_search_names, mock_navigate):
        """Test the integration of processing searches and lists."""
        # Setup mock returns
        mock_get_search_names.return_value = ["Search1", "Search2"]
        mock_get_list_names.return_value = ["List1", "List2"]
        
        # Call the method
        self.automation.process_searches_and_lists()
        
        # Assertions
        self.assertEqual(mock_navigate.call_count, 2)
        mock_get_search_names.assert_called_once()
        self.assertEqual(mock_load_search.call_count, 2)
        self.assertEqual(mock_save_list.call_count, 4)  # 2 for searches, 2 for lists
        mock_get_list_names.assert_called_once()
        self.assertEqual(mock_load_list.call_count, 2)
    
    @patch.object(VoterDataAutomation, 'initialize')
    @patch.object(VoterDataAutomation, 'download_and_upload_files')
    @patch.object(VoterDataAutomation, 'process_searches_and_lists')
    @patch.object(VoterDataAutomation, 'cleanup')
    def test_full_process_integration(self, mock_cleanup, mock_process, mock_download, mock_initialize):
        """Test the integration of the full automation process."""
        # Call the method
        self.automation.run_full_process()
        
        # Assertions
        mock_initialize.assert_called_once()
        mock_download.assert_called_once()
        mock_process.assert_called_once()
        mock_cleanup.assert_called_once()
    
    @patch('utils.start_driver')
    @patch('utils.get_page')
    @patch('utils.login_to_page')
    @patch('voter_data_downloader.VoterDataDownloader')
    @patch('van_file_manager.VANFileManager')
    @patch('van_search_list_manager.VANSearchListManager')
    def test_initialization_integration(self, mock_search_list_manager_class, mock_file_manager_class, 
                                       mock_downloader_class, mock_login, mock_get_page, mock_start_driver):
        """Test the integration of initialization components."""
        # Setup mock returns
        mock_driver = MagicMock()
        mock_start_driver.return_value = mock_driver
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_file_manager = MagicMock()
        mock_file_manager_class.return_value = mock_file_manager
        mock_search_list_manager = MagicMock()
        mock_search_list_manager_class.return_value = mock_search_list_manager
        
        # Create a fresh automation object
        automation = VoterDataAutomation()
        
        # Call the method
        automation.initialize()
        
        # Assertions
        mock_start_driver.assert_called_once()
        mock_get_page.assert_called_once_with(mock_driver)
        mock_login.assert_called_once_with(mock_driver)
        mock_downloader_class.assert_called_once()
        mock_file_manager_class.assert_called_once_with(mock_driver)
        mock_search_list_manager_class.assert_called_once_with(mock_driver)
        self.assertEqual(automation.driver, mock_driver)
        self.assertEqual(automation.downloader, mock_downloader)
        self.assertEqual(automation.file_manager, mock_file_manager)
        self.assertEqual(automation.search_list_manager, mock_search_list_manager)


if __name__ == '__main__':
    unittest.main()