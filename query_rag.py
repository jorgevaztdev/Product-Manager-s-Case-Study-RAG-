import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AISearchQuery:
    def __init__(self):
        """Initialize AI Search client."""
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        self.api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        self.ai_search_name = os.getenv('AI_SEARCH_NAME')
        
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}"
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    def query(self, question):
        """
        Query the AI Search instance.
        
        Args:
            question (str): The question to ask
            
        Returns:
            dict: The response from AI Search
        """
        try:
            # Construct the API endpoint for AI Search
            url = f"{self.base_url}/autorag/rags/{self.ai_search_name}/ai-search"
            
            payload = {
                "query": question
            }
            
            print(f"Querying AI Search: {question}")
            response = requests.post(url, json=payload, headers=self.headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result
            
        except requests.exceptions.HTTPError as e:
            # Try to get more details from the error response
            try:
                error_detail = e.response.json()
                print(f"Error querying AI Search: {error_detail}")
                return {'error': str(e), 'details': error_detail}
            except:
                print(f"Error querying AI Search: {str(e)}")
                return {'error': str(e)}
        except Exception as e:
            print(f"Error querying AI Search: {str(e)}")
            return {'error': str(e)}

# Example usage
if __name__ == "__main__":
    query_client = AISearchQuery()
    
    # Ask a question about your uploaded content
    question = "What is AI Search and how does it work?"
    result = query_client.query(question)
    
    print("\nAnswer:")
    print(result)