# Building a RAG POC with Cloudflare AI Search - Python Guide

This guide will walk you through creating a Proof of Concept (POC) for a RAG (Retrieval-Augmented Generation) system using Python and Cloudflare's AI Search.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Implementation](#implementation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Overview

We'll build a system that:
1. Fetches and renders web pages
2. Stores content in Cloudflare R2
3. Uses Cloudflare AI Search to query the content

## Prerequisites

### Software Requirements
- Python 3.8 or higher
- Node.js and npm (for Wrangler CLI)
- A Cloudflare account

### Step 1: Install Required Software

```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Linux/Mac

# Install Python packages
pip install requests cloudflare beautifulsoup4 python-dotenv boto3

# Install Wrangler (Cloudflare CLI)
npm install -g wrangler

# Login to Cloudflare
wrangler login
```

### Step 2: Create R2 Bucket

```bash
# Create an R2 bucket for storing HTML content
wrangler r2 bucket create html-bucket
```

### Step 3: Get Cloudflare Credentials

You'll need the following credentials:

1. **Account ID**
   ```bash
   wrangler whoami
   ```
   Look for "Account ID" in the output.

2. **R2 API Tokens**
   ```bash
   wrangler r2 bucket credentials create html-bucket --access-key-name my-access-key
   ```
   Save the Access Key ID and Secret Access Key - you'll need them!

3. **API Token** (for AI Search)
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
   - Navigate to: My Profile → API Tokens
   - Create Token → Use template "Edit Cloudflare Workers"
   - Or create custom token with AI permissions

## Setup Instructions

### Step 4: Create Project Structure

```bash
# Create project directory
mkdir rag-poc
cd rag-poc

# Create necessary files
touch .env main.py upload_to_r2.py query_rag.py
```

### Step 5: Configure Environment Variables

Create a `.env` file with your credentials:

```env
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
R2_ACCESS_KEY_ID=your_access_key_id_here
R2_SECRET_ACCESS_KEY=your_secret_access_key_here
R2_BUCKET_NAME=html-bucket
AI_SEARCH_NAME=my-rag
CLOUDFLARE_API_TOKEN=your_api_token_here
```

**Important:** Replace all placeholder values with your actual credentials from Step 3.

## Implementation

### File 1: upload_to_r2.py

This script fetches web pages and uploads them to R2 storage.

**What it does:**
- Fetches HTML content from URLs
- Cleans and parses the HTML using BeautifulSoup
- Uploads content to Cloudflare R2 bucket
- Creates unique keys for each uploaded file

**Key concepts:**
- `boto3`: AWS SDK that works with R2 (S3-compatible)
- `BeautifulSoup`: Parses and cleans HTML content
- `requests`: Fetches web pages

### File 2: query_rag.py

This script queries your AI Search instance.

**What it does:**
- Sends questions to Cloudflare AI Search
- Retrieves answers based on your uploaded content
- Handles API authentication

**Key concepts:**
- REST API calls using `requests`
- Bearer token authentication
- JSON payload formatting

### File 3: main.py

The main orchestration script that combines everything.

**What it does:**
- Demonstrates the complete workflow
- Uploads multiple URLs
- Queries the AI Search instance
- Shows example questions and answers

## Usage

### Step 6: Upload Content to R2

First, test uploading a single page:

```bash
python upload_to_r2.py
```

You should see output like:
```
Fetching content from: https://...
Uploading to R2 with key: developers.cloudflare.com_20251108_143022.html

Result:
{'success': True, 'message': 'Page fetched and stored successfully', ...}
```

### Step 7: Create AI Search Instance

**Manual steps in Cloudflare Dashboard:**

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to: AI → AI Search
3. Click **"Create AI Search"**
4. Configure:
   - Name: `my-rag`
   - Data Source: Select your `html-bucket`
   - Click **"Create"**
5. Wait for indexing to complete (may take a few minutes)

### Step 8: Query Your RAG System

Once AI Search is ready:

```bash
# Test a single query
python query_rag.py

# Or run the full demo
python main.py
```

## Understanding the Code

### How R2 Upload Works

```python
# 1. Initialize S3-compatible client
s3_client = boto3.client(
    's3',
    endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

# 2. Fetch webpage
response = requests.get(url)

# 3. Upload to R2
s3_client.put_object(
    Bucket=bucket_name,
    Key=unique_key,
    Body=html_content
)
```

### How AI Search Query Works

```python
# 1. Prepare API request
url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/autorag/{ai_search_name}/search"

# 2. Send query
payload = {"query": "Your question here"}
response = requests.post(url, json=payload, headers=headers)

# 3. Extract answer
result = response.json()
answer = result['result']['answer']
```

## Customization Options

### Adding More URLs

Edit `main.py` and add URLs to the list:

```python
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]
```

### Improving HTML Parsing

Modify `upload_to_r2.py` to extract specific content:

```python
# Extract only main content
soup = BeautifulSoup(response.content, 'html.parser')

# Remove unwanted elements
for element in soup(['script', 'style', 'nav', 'footer']):
    element.decompose()

# Get clean text
main_content = soup.get_text(separator='\n', strip=True)
```

### Custom Questions

Modify the questions list in `main.py`:

```python
questions = [
    "What is the main topic?",
    "How do I get started?",
    "What are the prerequisites?",
]
```

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Solution: Install missing packages
pip install requests beautifulsoup4 python-dotenv boto3
```

**2. R2 Access Denied**
- Verify credentials in `.env` file
- Check that R2 API token has correct permissions
- Confirm bucket name matches

**3. AI Search Not Found**
- Ensure AI Search instance name matches `AI_SEARCH_NAME` in `.env`
- Verify API token has AI permissions
- Wait for indexing to complete

**4. Connection Errors**
```bash
# Check your internet connection
ping cloudflare.com

# Verify API endpoints are accessible
curl https://api.cloudflare.com/client/v4/user
```

**5. Empty Responses**
- Wait for AI Search indexing to complete
- Check that content was uploaded successfully
- Verify R2 bucket is set as AI Search data source

### Debug Mode

Add debug output to see what's happening:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Checking R2 Contents

List files in your R2 bucket:

```bash
wrangler r2 object list html-bucket
```

## Next Steps

### Enhance Your POC

1. **Add More Content Sources**
   - Crawl entire websites
   - Add PDF support
   - Include documentation sites

2. **Build a Web Interface**
   ```bash
   pip install flask
   # Create a simple web UI for queries
   ```

3. **Improve Query Quality**
   - Add context to questions
   - Implement conversation history
   - Use prompt engineering techniques

4. **Add Monitoring**
   - Log all queries and responses
   - Track performance metrics
   - Monitor API usage

5. **Production Readiness**
   - Add error handling and retries
   - Implement rate limiting
   - Set up proper logging
   - Add unit tests

## Additional Resources

- [Cloudflare AI Search Documentation](https://developers.cloudflare.com/ai-search/)
- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [Python Requests Documentation](https://docs.python-requests.org/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Architecture Diagram

```
┌─────────────┐
│  Web Pages  │
└──────┬──────┘
       │ fetch
       ▼
┌─────────────────┐
│ upload_to_r2.py │
└──────┬──────────┘
       │ upload
       ▼
┌─────────────────┐
│  R2 Bucket      │
└──────┬──────────┘
       │ index
       ▼
┌─────────────────┐
│  AI Search      │
└──────┬──────────┘
       │ query
       ▼
┌─────────────────┐
│  query_rag.py   │
└─────────────────┘
```

## License

This is a POC for educational purposes. Modify and use as needed for your projects.

---

**Questions?** Review the troubleshooting section or check the Cloudflare documentation for more details.