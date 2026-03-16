import logging
import datetime
import requests
from pathlib import Path

class VoterDataDownloader:
    """
    A class for downloading VoterData files from the API.
    
    This class handles downloading VoterData files from the specified API endpoint,
    saving them to a local directory, and managing the download process.
    """
    
    def __init__(self, base_url="https://vat.flddc.org/API/VoterData/", output_directory="../io/api_downloads"):
        """
        Initialize the VoterDataDownloader.
        
        Args:
            base_url (str): The base URL for the API endpoint.
            output_directory (str): The directory where downloaded files will be saved.
        """
        # Configure logging - Now using getLogger only to respect the orchestrator's config
        self.logger = logging.getLogger('VoterDataDownloader')
        
        self.base_url = base_url
        self.output_directory = Path(output_directory)
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
        output_path = self.output_directory / f"{file_id}_VoterData.csv"
        
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
            return str(output_path)
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error downloading {file_id}: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error downloading {file_id}: {e}")
            raise
        except IOError as e:
            self.logger.error(f"IO error saving {file_id}: {e}")
            raise
    
    def should_download_file(self, file_id):
        """
        Check if a file should be downloaded based on its last modification date.
        
        Args:
            file_id (str): The ID of the file to check.
            
        Returns:
            bool: True if the file should be downloaded, False otherwise.
        """
        output_path = self.output_directory / f"{file_id}_VoterData.csv"
        
        # If the file doesn't exist, it should be downloaded
        if not output_path.exists():
            self.logger.info(f"File {file_id} does not exist, will download")
            return True
        
        # Get the file's last modification time
        mod_time = datetime.datetime.fromtimestamp(output_path.stat().st_mtime)
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # If the file was modified today, don't download it again
        if mod_time >= today:
            self.logger.info(f"File {file_id} was already downloaded today ({mod_time.strftime('%Y-%m-%d')}), skipping")
            return False
        
        # If the file is older than today, download it
        self.logger.info(f"File {file_id} is outdated (last modified: {mod_time.strftime('%Y-%m-%d')}), will download")
        return True
    
    def download_all_files(self, file_ids):
        """
        Download multiple VoterData files, but only if they haven't been downloaded today.
        
        Args:
            file_ids (list): A list of file IDs to download.
            
        Returns:
            list: A list of paths to the downloaded files.
            
        Raises:
            Exception: If any download fails, the exception is propagated.
        """
        self.logger.info(f"Starting download of up to {len(file_ids)} files")
        downloaded_files = []
        skipped_files = []
        
        for file_id in file_ids:
            try:
                # Check if the file should be downloaded
                if self.should_download_file(file_id):
                    file_path = self.download_file(file_id)
                    downloaded_files.append(file_path)
                else:
                    # If the file shouldn't be downloaded, add it to the list of skipped files
                    skipped_files.append(str(self.output_directory / f"{file_id}_VoterData.csv"))
            except Exception as e:
                self.logger.error(f"Error downloading file {file_id}: {e}")
                raise
        
        self.logger.info(f"Successfully downloaded {len(downloaded_files)} files, skipped {len(skipped_files)} files")
        
        # Return both downloaded and skipped files
        return downloaded_files + skipped_files
    
    def _ensure_output_directory(self):
        """
        Ensure the output directory exists, creating it if necessary.
        """
        if not self.output_directory.exists():
            self.output_directory.mkdir(parents=True, exist_ok=True)
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