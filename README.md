### AI Compliance Assistant: RAG-based Logistics Search

A Product Case Study in Retrieval Augmented Generation (RAG)

## 🎯 The Problem

In cross-border logistics (a key focus of my background at Nowports), compliance managers spend 4+ hours per week manually searching through dense PDF customs regulations and Harmonized Tariff Schedules.

## 💡 The Solution

I built this "RAG Compliance Assistant" to reduce information retrieval time from minutes to seconds. By indexing documentation using Cloudflare's Vector Search, users can ask natural language questions ("Can I ship lithium batteries via air freight?") and receive cited, context-aware answers.

## 🚀 Key Metrics (Success Criteria)

Retrieval Latency: <3 seconds per query (achieved via Cloudflare Edge execution).

Accuracy: Targeted 90% retrieval accuracy on a "Golden Dataset" of 20 common compliance questions.

Cost Efficiency: $0 operational cost for MVP using Cloudflare's integrated AI/R2 stack (vs. AWS separate components).# RAG POC with Cloudflare AI Search

A Python-based Proof of Concept (POC) demonstrating Retrieval-Augmented Generation (RAG) using Cloudflare's AI Search, R2 storage, and natural language processing.

## 📋 Overview

This project demonstrates how to build a complete RAG system that:
1. **Fetches web content** from specified URLs
2. **Stores content** in Cloudflare R2 (object storage)
3. **Indexes content** using Cloudflare AI Search (vector database)
4. **Queries content** with natural language questions
5. **Generates AI-powered answers** from your indexed documents

## 🏗️ Architecture

```
┌─────────────┐
│  Web Pages  │
└──────┬──────┘
       │ fetch (BeautifulSoup)
       ▼
┌─────────────────┐
│ upload_to_r2.py │
└──────┬──────────┘
       │ upload (boto3)
       ▼
┌─────────────────┐
│  R2 Bucket      │
└──────┬──────────┘
       │ index (automated)
       ▼
┌─────────────────┐
│  AI Search      │ (665 vectors)
└──────┬──────────┘
       │ query (REST API)
       ▼
┌─────────────────┐
│  query_rag.py   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  AI Response    │
└─────────────────┘
```

## 🚀 Features

- **Automatic Content Fetching**: Retrieves and parses HTML from any URL
- **Cloud Storage**: Stores content in Cloudflare R2 with unique keys
- **Vector Search**: Indexes content using AI embeddings for semantic search
- **Natural Language Queries**: Ask questions in plain English
- **AI-Generated Answers**: Get contextual answers from your documents
- **Configurable**: Easy to add more URLs and customize queries

## 📁 Project Structure

```
ragPOC/
├── .env                    # Environment variables (credentials)
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── Instructions.md        # Detailed setup guide
├── README.md             # This file
├── main.py               # Main orchestration script
├── upload_to_r2.py       # R2 upload functionality
├── query_rag.py          # AI Search query functionality
└── test_r2_connection.py # R2 connection test script
```

## 🔧 Prerequisites

- Python 3.8 or higher
- A Cloudflare account
- Node.js and npm (for Wrangler CLI)

## 📦 Installation

### 1. Clone and Setup Virtual Environment

```bash
cd ragPOC
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Wrangler CLI (Cloudflare CLI)

```bash
npm install -g wrangler
wrangler login
```

## ⚙️ Configuration

### 1. Create R2 Bucket

```bash
wrangler r2 bucket create html-bucket
```

### 2. Get Cloudflare Credentials

You'll need:
- **Account ID**: Found in Cloudflare Dashboard
- **R2 Access Keys**: Dashboard → R2 → Manage R2 API Tokens
- **API Token**: Dashboard → My Profile → API Tokens (with AI permissions)

### 3. Configure Environment Variables

Create/update `.env` file:

```env
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
R2_ACCESS_KEY_ID=your_r2_access_key_here
R2_SECRET_ACCESS_KEY=your_r2_secret_key_here
R2_BUCKET_NAME=html-bucket
AI_SEARCH_NAME=your-ai-search-instance-name
CLOUDFLARE_API_TOKEN=your_api_token_here
```

### 4. Create AI Search Instance

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → **AI** → **AI Search**
2. Click **"Create AI Search"**
3. Configure:
   - **Name**: Use the same name as in your `.env` file
   - **Data Source**: Select `html-bucket`
4. Click **"Create"**
5. Wait for indexing to complete (5-10 minutes)

## 🎮 Usage

### Run Complete RAG System

```bash
python main.py
```

This will:
1. Upload web pages to R2
2. Wait for AI Search to index (if needed)
3. Run example queries
4. Display AI-generated answers

### Test Individual Components

**Test R2 Connection:**
```bash
python test_r2_connection.py
```

**Test Content Upload:**
```bash
python upload_to_r2.py
```

**Test AI Search Query:**
```bash
python query_rag.py
```

## 💡 How It Works

### 1. Content Upload (`upload_to_r2.py`)

```python
# Fetches HTML from URL
response = requests.get(url)

# Parses and cleans HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Uploads to R2 with unique key
s3_client.put_object(
    Bucket='html-bucket',
    Key='unique_key.html',
    Body=html_content
)
```

### 2. AI Search Indexing (Automatic)

- Cloudflare AI Search monitors your R2 bucket
- Automatically extracts text from HTML files
- Creates vector embeddings using AI models
- Stores vectors in Vectorize database
- Updates index when content changes

### 3. Natural Language Query (`query_rag.py`)

```python
# Send query to AI Search
response = requests.post(
    f"{base_url}/autorag/rags/{ai_search_name}/ai-search",
    json={"query": "What is AI Search?"},
    headers={"Authorization": f"Bearer {api_token}"}
)

# Get AI-generated answer
answer = response.json()['result']['response']
```

## 📊 Example Output

```
== RAG POC with Cloudflare R2 and AI Search ==

Fetching content from: https://developers.cloudflare.com/ai-search/...
Uploading to R2 with key: developers.cloudflare.com_20251111_144853.html
✓ Uploaded developers.cloudflare.com_20251111_144853.html

Step 2: Querying AI Search...

❓ Question: What is AI Search?
💡 Answer: AI Search is Cloudflare's managed search service, which allows 
you to connect your data, such as websites or unstructured content, and 
automatically creates a continuously updating index that you can query 
with natural language in your applications or AI agents.

❓ Question: How do I use Browser Rendering with AI Search?
💡 Answer: To use Browser Rendering with AI Search, follow these steps:
1. Render your website using Cloudflare's Browser Rendering API.
2. Store the rendered HTML in R2.
3. Connect it to AI Search for querying...
```

## 🎯 Customization

### Add More URLs to Index

Edit `main.py`:

```python
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://your-docs.com/guide",
]
```

### Add Custom Questions

Edit `main.py`:

```python
questions = [
    "How do I get started?",
    "What are the pricing options?",
    "How does authentication work?",
]
```

### Modify Content Parsing

Edit `upload_to_r2.py` to extract specific content:

```python
# Remove unwanted elements
for element in soup(['script', 'style', 'nav', 'footer']):
    element.decompose()

# Extract only main content
main_content = soup.find('main') or soup
```

## 🔍 API Details

### R2 API (S3-Compatible)

- **Endpoint**: `https://{account_id}.r2.cloudflarestorage.com`
- **Authentication**: Access Key ID + Secret Access Key
- **SDK**: boto3 (AWS SDK for Python)

### AI Search API

- **Endpoint**: `https://api.cloudflare.com/client/v4/accounts/{account_id}/autorag/rags/{name}/ai-search`
- **Authentication**: Bearer token
- **Method**: POST
- **Request**: `{"query": "your question"}`
- **Response**: Includes AI-generated answer and source documents

## 🛠️ Troubleshooting

### R2 Access Denied
- Verify R2 Access Keys are correct in `.env`
- Ensure bucket name matches exactly
- Check credentials have proper permissions

### AI Search 400 Error
- Confirm API token has AI Search permissions
- Verify AI Search instance name matches `.env`
- Check instance is fully indexed (no pending jobs)

### Connection Timeout
- Increase timeout in `query_rag.py`: `timeout=60`
- Check internet connection
- Verify Cloudflare API is accessible

### Import Errors
```bash
pip install -r requirements.txt
```

## 📚 Resources

- [Cloudflare AI Search Documentation](https://developers.cloudflare.com/ai-search/)
- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [Cloudflare API Reference](https://developers.cloudflare.com/api/)
- [Python Requests Documentation](https://docs.python-requests.org/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/)

## 🔐 Security Notes

- **Never commit `.env` file** to version control
- Keep API tokens and access keys secure
- Rotate credentials regularly
- Use scoped API tokens with minimum required permissions
- Monitor API usage in Cloudflare Dashboard

## 📈 Performance

Current Setup:
- **R2 Storage**: Unlimited objects (pay per storage/operations)
- **AI Search**: 665 vectors indexed
- **Query Response**: ~3-5 seconds average
- **Indexing Time**: ~5-10 minutes for initial setup

## 🚀 Next Steps

1. **Add More Content**: Index documentation, blogs, wikis
2. **Build Web Interface**: Create Flask/FastAPI app
3. **Add Authentication**: Secure your API endpoints
4. **Implement Caching**: Cache frequent queries
5. **Add Monitoring**: Track usage and performance
6. **Deploy**: Host on Cloudflare Workers or Pages

## 📝 License

This is a POC (Proof of Concept) for educational purposes.

## 🤝 Contributing

This is a learning project. Feel free to:
- Add features
- Improve error handling
- Enhance documentation
- Share improvements

## 📧 Support

For Cloudflare-specific questions:
- [Cloudflare Community](https://community.cloudflare.com/)
- [Cloudflare Discord](https://discord.cloudflare.com/)
- [Support Center](https://support.cloudflare.com/)

---

**Built with ❤️ using Cloudflare AI Search, R2, and Python**

Last Updated: November 11, 2025
