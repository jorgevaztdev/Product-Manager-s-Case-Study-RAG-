"""
RAG POC - Main Script
This script demostrates how to:
1. Upload web content to Cloudflare R2.
2. Query it using Cloudflare AI Search.
"""

import os
from dotenv import load_dotenv
from upload_to_r2 import HTMLFetcher 
from query_rag import AISearchQuery

def main():
    """Main function to run RAG POC."""
    load_dotenv()
    
    print("== RAG POC with Cloudflare R2 and AI Search ==\n")
    # Step 1: Upload web content to Cloudflare R2
    fetcher = HTMLFetcher()

    #list of URLs to index
    urls = ["https://developers.cloudflare.com/ai-search/tutorial/brower-rendering-autorag-tutorial/",
        "https://developers.cloudflare.com/ai-search/get-started/",
    ]

    for url in urls:
        result = fetcher.fetch_and_upload(url)
        if result ['success']:
            print(f"Uploaded {result['key']}")
        else:
            print(f"Failed to upload {url}: {result['message']}")
    
    print("\n"+"="*50+"\n")
    print("Content uploaded! Now you need to:")
    print("1. Go to Cloudflare Dashboard > AI > AI Search")
    print("2. Create a new AI Search instance named 'morning-moon-64f5'")
    print("3. Select your 'html-bucket' as the data source")
    print("4. Wait for indexing to complete")
    print("="*50 + "\n")

    input("Press Enter once AI Search is ready...")
    
    # Step 2: Query the RAG
    print("\nStep 2: Querying AI Search...")
    query_client = AISearchQuery()
    
    questions = [
        "What is AI Search?",
        "How do I use Browser Rendering with AI Search?",
        "What are the steps to create an AI Search instance?"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        result = query_client.query(question)
        
        if 'error' not in result:
            # Extract answer from response
            if result.get('success'):
                response = result.get('result', {}).get('response', 'No answer found')
                print(f"💡 Answer: {response}")
            else:
                print(f"❌ No answer found")
        else:
            print(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    main()
