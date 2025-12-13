import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import will be available after we create the module
# from van_file_manager import VANFileManager

class TestVANFileManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a mock WebDriver
        self.mock_driver = MagicMock()
        
        # Import the module here to ensure it's reloaded for each test
        from van_file_manager import VANFileManager
        self.file_manager = VANFileManager(self.mock_driver)
    
    @patch('utils.expect_by_XPATH')
    def test_navigate_to_file_folder(self, mock_expect_by_xpath):
        """Test navigation to a specific folder in VAN."""
        # Setup mock element
        mock_element = MagicMock()
        mock_expect_by_xpath.return_value = mock_element
        
        # Call the method
        self.file_manager.navigate_to_file_folder("VAT Lists (xx)")
        
        # Assertions
        mock_expect_by_xpath.assert_called_with(self.mock_driver, "//a[contains(text(), 'VAT Lists (xx)')]")
        mock_element.click.assert_called_once()
    
    @patch('utils.expect_by_id')
    @patch('utils.expect_by_XPATH')
    @patch('utils.handle_alert')
    def test_delete_files(self, mock_handle_alert, mock_expect_by_xpath, mock_expect_by_id):
        """Test deletion of files in VAN."""
        # Setup mock elements
        mock_checkbox = MagicMock()
        mock_delete_button = MagicMock()
        mock_confirm_button = MagicMock()
        
        # Setup mock returns for different calls
        mock_expect_by_xpath.side_effect = [mock_checkbox]
        mock_expect_by_id.side_effect = [mock_delete_button, mock_confirm_button]
        
        # Call the method
        self.file_manager.delete_files(["G01_VoterData"])
        
        # Assertions
        mock_expect_by_xpath.assert_called_with(
            self.mock_driver, 
            "//td[contains(text(), 'G01_VoterData')]/preceding-sibling::td/input[@type='checkbox']"
        )
        mock_checkbox.click.assert_called_once()
        mock_expect_by_id.assert_any_call(self.mock_driver, "deleteButton")
        mock_delete_button.click.assert_called_once()
        mock_expect_by_id.assert_any_call(self.mock_driver, "confirmDeleteButton")
        mock_confirm_button.click.assert_called_once()
        mock_handle_alert.assert_called_once_with(self.mock_driver)
    
    @patch('utils.expect_by_id')
    @patch('utils.expect_by_XPATH')
    def test_bulk_upload_files(self, mock_expect_by_xpath, mock_expect_by_id):
        """Test bulk upload of files to VAN."""
        # Setup mock elements
        mock_upload_button = MagicMock()
        mock_file_input = MagicMock()
        mock_submit_button = MagicMock()
        
        # Setup mock returns
        mock_expect_by_id.side_effect = [mock_upload_button, mock_file_input, mock_submit_button]
        
        # Call the method
        file_paths = ["path/to/G01_VoterData.csv", "path/to/G02_VoterData.csv"]
        self.file_manager.bulk_upload_files(file_paths)
        
        # Assertions
        mock_expect_by_id.assert_any_call(self.mock_driver, "uploadButton")
        mock_upload_button.click.assert_called_once()
        mock_expect_by_id.assert_any_call(self.mock_driver, "fileInput")
        mock_file_input.send_keys.assert_called_once()
        # Check that the file paths were passed to send_keys
        args, _ = mock_file_input.send_keys.call_args
        self.assertEqual(len(args), 1)
        self.assertTrue(all(path in args[0] for path in file_paths))
        mock_expect_by_id.assert_any_call(self.mock_driver, "submitUploadButton")
        mock_submit_button.click.assert_called_once()
    
    @patch('utils.expect_by_XPATH')
    def test_verify_upload_success_true(self, mock_expect_by_xpath):
        """Test verification of successful upload."""
        # Setup mock element that exists (upload successful)
        mock_element = MagicMock()
        mock_expect_by_xpath.return_value = mock_element
        
        # Call the method
        result = self.file_manager.verify_upload_success()
        
        # Assertions
        self.assertTrue(result)
        mock_expect_by_xpath.assert_called_with(
            self.mock_driver, 
            "//div[contains(text(), 'Upload completed successfully')]"
        )
    
    @patch('utils.expect_by_XPATH')
    def test_verify_upload_success_false(self, mock_expect_by_xpath):
        """Test verification of failed upload."""
        # Setup mock to raise exception (element not found)
        from selenium.common.exceptions import TimeoutException
        mock_expect_by_xpath.side_effect = TimeoutException("Element not found")
        
        # Call the method
        result = self.file_manager.verify_upload_success()
        
        # Assertions
        self.assertFalse(result)
        mock_expect_by_xpath.assert_called_with(
            self.mock_driver, 
            "//div[contains(text(), 'Upload completed successfully')]"
        )


if __name__ == '__main__':
    unittest.main()