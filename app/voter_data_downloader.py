import os
import requests
import logging

class VoterDataDownloader:
    """
    A class for downloading VoterData files from the API.
    
    This class handles downloading VoterData files from the specified API endpoint,
    saving them to a local directory, and managing the download process.
    """
    
    def __init__(self, base_url="https://vat.flddc.org/API/VoterData/", output_directory="../io/Input"):
        """
        Initialize the VoterDataDownloader.
        
        Args:
            base_url (str): The base URL for the API endpoint.
            output_directory (str): The directory where downloaded files will be saved.
        """
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('VoterDataDownloader')
        
        self.base_url = base_url
        self.output_directory = output_directory
        self._ensure_output_directory()
    
    def download_file(self, file_id):
        """
        Download a single VoterData file.
        
        Args:
            file_id (str): The ID of the file to download (e.g., "G01").
            
        Returns:
            str: The path to the downloaded file.
            
        Raises:
            requests.exceptions.HTTPError: If the HTTP request fails.
            requests.exceptions.ConnectionError: If there's a connection error.
            IOError: If there's an error writing the file.
        """
        url = self._build_url(file_id)
        output_path = os.path.join(self.output_directory, f"{file_id}_VoterData.csv")
        
        self.logger.info(f"Downloading file {file_id} from {url}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # For test mocks that don't have iter_content
            if hasattr(response, 'iter_content'):
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # Filter out keep-alive chunks
                            f.write(chunk)
            else:
                # Handle mock responses in tests
                with open(output_path, 'wb') as f:
                    f.write(response.content)
            
            self.logger.info(f"Successfully downloaded {file_id} to {output_path}")
            return output_path
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error downloading {file_id}: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error downloading {file_id}: {e}")
            raise
        except IOError as e:
            self.logger.error(f"IO error saving {file_id}: {e}")
            raise
    
    def download_all_files(self, file_ids):
        """
        Download multiple VoterData files.
        
        Args:
            file_ids (list): A list of file IDs to download.
            
        Returns:
            list: A list of paths to the downloaded files.
            
        Raises:
            Exception: If any download fails, the exception is propagated.
        """
        self.logger.info(f"Starting download of {len(file_ids)} files")
        downloaded_files = []
        
        for file_id in file_ids:
            try:
                file_path = self.download_file(file_id)
                downloaded_files.append(file_path)
            except Exception as e:
                self.logger.error(f"Error downloading file {file_id}: {e}")
                raise
        
        self.logger.info(f"Successfully downloaded {len(downloaded_files)} files")
        return downloaded_files
    
    def _ensure_output_directory(self):
        """
        Ensure the output directory exists, creating it if necessary.
        """
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
            self.logger.info(f"Created output directory: {self.output_directory}")
    
    def _build_url(self, file_id):
        """
        Build the URL for a specific file.
        
        Args:
            file_id (str): The ID of the file.
            
        Returns:
            str: The complete URL for the file.
        """
        return f"{self.base_url}{file_id}"


if __name__ == "__main__":
    # Example usage
    downloader = VoterDataDownloader()
    try:
        # Download a single file
        file_path = downloader.download_file("G01")
        print(f"Downloaded file to: {file_path}")
        
        # Download multiple files
        file_ids = ["G01", "G02", "G03"]
        file_paths = downloader.download_all_files(file_ids)
        print(f"Downloaded files to: {file_paths}")
    except Exception as e:
        print(f"Error: {e}")