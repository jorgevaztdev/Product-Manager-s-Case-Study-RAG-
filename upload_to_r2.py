import os
import requests
from datetime import datetime
from urllib.parse import urlparse
import boto3
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

class HTMLFetcher:
    def __init__(self):
        """Initialize the HTML fetcher with R2 credentials."""
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        self.access_key = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.bucket_name = os.getenv('R2_BUCKET_NAME')
        
        # Initialize R2 client (R2 uses S3-compatible API)
        self.s3_client = boto3.client(
            's3',
            endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name='auto'
        )
    
    def fetch_and_upload(self, url):
        """
        Fetch HTML content from a URL and upload it to R2.
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            dict: Response with success status and key
        """
        try:
            print(f"Fetching content from: {url}")
            
            # Fetch the webpage
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML (optional: clean it up)
            soup = BeautifulSoup(response.content, 'html.parser')
            html_content = str(soup)
            
            # Create a unique key for R2
            parsed_url = urlparse(url)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            key = f"{parsed_url.hostname}_{timestamp}.html"
            
            # Upload to R2
            print(f"Uploading to R2 with key: {key}")
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=html_content.encode('utf-8'),
                ContentType='text/html'
            )
            
            return {
                'success': True,
                'message': 'Page fetched and stored successfully',
                'key': key,
                'url': url
            }
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }

# Example usage
if __name__ == "__main__":
    fetcher = HTMLFetcher()
    
    # Test with the Cloudflare tutorial page
    test_url = "https://developers.cloudflare.com/ai-search/tutorial/brower-rendering-autorag-tutorial/"
    result = fetcher.fetch_and_upload(test_url)
    
    print("\nResult:")
    print(result)