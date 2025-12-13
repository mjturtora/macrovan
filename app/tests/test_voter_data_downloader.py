import unittest
from unittest.mock import patch, MagicMock
import os
import requests
import sys
import shutil

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import will be available after we create the module
# from voter_data_downloader import VoterDataDownloader

class TestVoterDataDownloader(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test."""
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_output")
        self.base_url = "https://vat.flddc.org/API/VoterData/"
        
        # Import the module here to ensure it's reloaded for each test
        from voter_data_downloader import VoterDataDownloader
        self.downloader = VoterDataDownloader(base_url=self.base_url, output_directory=self.output_dir)
        
        # Create test directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def tearDown(self):
        """Clean up after each test."""
        # Clean up test files
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
    
    @patch('requests.get')
    def test_download_file_success(self, mock_get):
        """Test successful file download."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Test file content"
        mock_get.return_value = mock_response
        
        # Call the method
        file_path = self.downloader.download_file("G01")
        
        # Assertions
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(os.path.basename(file_path), "G01_VoterData.csv")
        with open(file_path, 'rb') as f:
            self.assertEqual(f.read(), b"Test file content")
        mock_get.assert_called_once_with(f"{self.base_url}G01", stream=True)
    
    @patch('requests.get')
    def test_download_file_http_error(self, mock_get):
        """Test handling of HTTP errors."""
        # Setup mock response for HTTP error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = mock_response
        
        # Call the method and check for exception
        with self.assertRaises(requests.exceptions.HTTPError):
            self.downloader.download_file("G01")
    
    @patch('requests.get')
    def test_download_file_connection_error(self, mock_get):
        """Test handling of connection errors."""
        # Setup mock for connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        # Call the method and check for exception
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.downloader.download_file("G01")
    
    @patch('voter_data_downloader.VoterDataDownloader.download_file')
    def test_download_all_files_success(self, mock_download_file):
        """Test successful download of multiple files."""
        # Setup mock to return file paths
        file_ids = ["G01", "G02", "G03"]
        expected_paths = [
            os.path.join(self.output_dir, "G01_VoterData.csv"),
            os.path.join(self.output_dir, "G02_VoterData.csv"),
            os.path.join(self.output_dir, "G03_VoterData.csv")
        ]
        
        mock_download_file.side_effect = expected_paths
        
        # Call the method
        result = self.downloader.download_all_files(file_ids)
        
        # Assertions
        self.assertEqual(result, expected_paths)
        self.assertEqual(mock_download_file.call_count, 3)
        mock_download_file.assert_any_call("G01")
        mock_download_file.assert_any_call("G02")
        mock_download_file.assert_any_call("G03")
    
    @patch('voter_data_downloader.VoterDataDownloader.download_file')
    def test_download_all_files_partial_failure(self, mock_download_file):
        """Test handling of partial download failures."""
        # Setup mock to succeed for first file, fail for second, succeed for third
        file_ids = ["G01", "G02", "G03"]
        
        def side_effect(file_id):
            if file_id == "G02":
                raise requests.exceptions.HTTPError("404 Client Error")
            return os.path.join(self.output_dir, f"{file_id}_VoterData.csv")
        
        mock_download_file.side_effect = side_effect
        
        # Call the method and check for exception
        with self.assertRaises(requests.exceptions.HTTPError):
            self.downloader.download_all_files(file_ids)
        
        # Verify first file was attempted
        mock_download_file.assert_any_call("G01")
    
    def test_ensure_output_directory(self):
        """Test creation of output directory."""
        # Remove the directory created in setUp
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        
        # Call the private method
        self.downloader._ensure_output_directory()
        
        # Verify directory was created
        self.assertTrue(os.path.exists(self.output_dir))
        self.assertTrue(os.path.isdir(self.output_dir))
    
    def test_build_url(self):
        """Test URL construction."""
        # Test URL construction
        file_id = "G05"
        expected_url = f"{self.base_url}G05"
        
        url = self.downloader._build_url(file_id)
        
        self.assertEqual(url, expected_url)


if __name__ == '__main__':
    unittest.main()