import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import will be available after we create the module
# from van_search_list_manager import VANSearchListManager

class TestVANSearchListManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a mock WebDriver
        self.mock_driver = MagicMock()
        
        # Import the module here to ensure it's reloaded for each test
        from van_search_list_manager import VANSearchListManager
        self.search_list_manager = VANSearchListManager(self.mock_driver)
    
    @patch('utils.expect_by_XPATH')
    def test_navigate_to_search_folder(self, mock_expect_by_xpath):
        """Test navigation to a search folder in VAN."""
        # Setup mock element
        mock_element = MagicMock()
        mock_expect_by_xpath.return_value = mock_element
        
        # Call the method
        self.search_list_manager.navigate_to_search_folder("VAT Searches")
        
        # Assertions
        mock_expect_by_xpath.assert_called_with(self.mock_driver, "//a[contains(text(), 'VAT Searches')]")
        mock_element.click.assert_called_once()
    
    @patch('utils.expect_by_id')
    @patch('utils.expect_by_XPATH')
    @patch('utils.handle_alert')
    def test_load_search(self, mock_handle_alert, mock_expect_by_xpath, mock_expect_by_id):
        """Test loading a saved search in VAN."""
        # Setup mock elements
        mock_search_input = MagicMock()
        mock_search_button = MagicMock()
        mock_search_result = MagicMock()
        
        # Setup mock returns
        mock_expect_by_id.side_effect = [mock_search_input, mock_search_button]
        mock_expect_by_xpath.return_value = mock_search_result
        
        # Call the method
        self.search_list_manager.load_search("Test Search")
        
        # Assertions
        mock_expect_by_id.assert_any_call(self.mock_driver, "searchNameInput")
        mock_search_input.send_keys.assert_called_once_with("Test Search")
        mock_expect_by_id.assert_any_call(self.mock_driver, "searchButton")
        mock_search_button.click.assert_called_once()
        mock_expect_by_xpath.assert_called_with(self.mock_driver, "//a[contains(text(), 'Test Search')]")
        mock_search_result.click.assert_called_once()
        mock_handle_alert.assert_called_once_with(self.mock_driver)
    
    @patch('utils.expect_by_id')
    @patch('utils.expect_by_XPATH')
    def test_save_list(self, mock_expect_by_xpath, mock_expect_by_id):
        """Test saving a list in VAN."""
        # Setup mock elements
        mock_save_button = MagicMock()
        mock_list_name_input = MagicMock()
        mock_folder_dropdown = MagicMock()
        mock_folder_option = MagicMock()
        mock_replace_checkbox = MagicMock()
        mock_submit_button = MagicMock()
        
        # Setup mock returns
        mock_expect_by_id.side_effect = [
            mock_save_button, mock_list_name_input, mock_folder_dropdown, mock_replace_checkbox, mock_submit_button
        ]
        mock_expect_by_xpath.return_value = mock_folder_option
        
        # Call the method
        self.search_list_manager.save_list("Test List", "VAT Lists (xx)", True)
        
        # Assertions
        mock_expect_by_id.assert_any_call(self.mock_driver, "saveListButton")
        mock_save_button.click.assert_called_once()
        mock_expect_by_id.assert_any_call(self.mock_driver, "listNameInput")
        mock_list_name_input.clear.assert_called_once()
        mock_list_name_input.send_keys.assert_called_once_with("Test List")
        mock_expect_by_id.assert_any_call(self.mock_driver, "folderDropdown")
        mock_folder_dropdown.click.assert_called_once()
        mock_expect_by_xpath.assert_called_with(self.mock_driver, "//option[contains(text(), 'VAT Lists (xx)')]")
        mock_folder_option.click.assert_called_once()
        mock_expect_by_id.assert_any_call(self.mock_driver, "replaceExistingCheckbox")
        mock_replace_checkbox.click.assert_called_once()
        mock_expect_by_id.assert_any_call(self.mock_driver, "submitSaveButton")
        mock_submit_button.click.assert_called_once()
    
    @patch('utils.expect_by_XPATH')
    @patch('utils.handle_alert')
    def test_load_list(self, mock_handle_alert, mock_expect_by_xpath):
        """Test loading a list in VAN."""
        # Setup mock elements
        mock_list_link = MagicMock()
        mock_expect_by_xpath.return_value = mock_list_link
        
        # Call the method
        self.search_list_manager.load_list("Test List", "VAT Lists (xx)")
        
        # Assertions
        mock_expect_by_xpath.assert_called_with(self.mock_driver, "//a[contains(text(), 'Test List')]")
        mock_list_link.click.assert_called_once()
        mock_handle_alert.assert_called_once_with(self.mock_driver)
    
    @patch('van_search_list_manager.VANSearchListManager.navigate_to_search_folder')
    @patch('van_search_list_manager.VANSearchListManager.get_search_names')
    @patch('van_search_list_manager.VANSearchListManager.load_search')
    @patch('van_search_list_manager.VANSearchListManager.save_list')
    def test_process_all_searches(self, mock_save_list, mock_load_search, mock_get_search_names, mock_navigate):
        """Test processing all searches in a folder."""
        # Setup test data
        search_names = ["Search1", "Search2", "Search3"]
        mock_get_search_names.return_value = search_names
        
        # Call the method
        self.search_list_manager.process_all_searches("VAT Searches", "VAT Lists (xx)")
        
        # Assertions
        mock_navigate.assert_called_once_with("VAT Searches")
        mock_get_search_names.assert_called_once()
        self.assertEqual(mock_load_search.call_count, 3)
        mock_load_search.assert_has_calls([call("Search1"), call("Search2"), call("Search3")])
        self.assertEqual(mock_save_list.call_count, 3)
        mock_save_list.assert_has_calls([
            call("Search1", "VAT Lists (xx)", True),
            call("Search2", "VAT Lists (xx)", True),
            call("Search3", "VAT Lists (xx)", True)
        ])
    
    @patch('van_search_list_manager.VANSearchListManager.navigate_to_search_folder')
    @patch('van_search_list_manager.VANSearchListManager.get_list_names')
    @patch('van_search_list_manager.VANSearchListManager.load_list')
    @patch('van_search_list_manager.VANSearchListManager.save_list')
    def test_process_all_lists(self, mock_save_list, mock_load_list, mock_get_list_names, mock_navigate):
        """Test processing all lists in a folder."""
        # Setup test data
        list_names = ["List1", "List2", "List3"]
        mock_get_list_names.return_value = list_names
        
        # Call the method
        self.search_list_manager.process_all_lists("VAT Lists (xx)")
        
        # Assertions
        mock_navigate.assert_called_once_with("VAT Lists (xx)")
        mock_get_list_names.assert_called_once()
        self.assertEqual(mock_load_list.call_count, 3)
        mock_load_list.assert_has_calls([
            call("List1", "VAT Lists (xx)"),
            call("List2", "VAT Lists (xx)"),
            call("List3", "VAT Lists (xx)")
        ])
        self.assertEqual(mock_save_list.call_count, 3)
        mock_save_list.assert_has_calls([
            call("List1", "VAT Lists (xx)", True),
            call("List2", "VAT Lists (xx)", True),
            call("List3", "VAT Lists (xx)", True)
        ])
    
    @patch('utils.expect_by_XPATH')
    def test_get_search_names(self, mock_expect_by_xpath):
        """Test getting search names from a folder."""
        # Setup mock elements
        mock_search_elements = [MagicMock(), MagicMock(), MagicMock()]
        for i, element in enumerate(mock_search_elements):
            element.text = f"Search{i+1}"
        
        mock_expect_by_xpath.return_value = mock_search_elements
        
        # Call the method
        result = self.search_list_manager.get_search_names()
        
        # Assertions
        expected_names = ["Search1", "Search2", "Search3"]
        self.assertEqual(result, expected_names)
        mock_expect_by_xpath.assert_called_with(self.mock_driver, "//a[contains(@class, 'searchName')]")
    
    @patch('utils.expect_by_XPATH')
    def test_get_list_names(self, mock_expect_by_xpath):
        """Test getting list names from a folder."""
        # Setup mock elements
        mock_list_elements = [MagicMock(), MagicMock(), MagicMock()]
        for i, element in enumerate(mock_list_elements):
            element.text = f"List{i+1}"
        
        mock_expect_by_xpath.return_value = mock_list_elements
        
        # Call the method
        result = self.search_list_manager.get_list_names()
        
        # Assertions
        expected_names = ["List1", "List2", "List3"]
        self.assertEqual(result, expected_names)
        mock_expect_by_xpath.assert_called_with(self.mock_driver, "//a[contains(@class, 'listName')]")


if __name__ == '__main__':
    unittest.main()