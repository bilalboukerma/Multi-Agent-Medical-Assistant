# Multi-Agent Medical Assistant Setup Guide

This guide will walk you through the process of setting up and running the Multi-Agent Medical Assistant project.

## Prerequisites

- Python 3.11+ installed
- Git installed
- Access to OpenRouter API or Azure OpenAI API

## Step 1: Clone the Repository

If you haven't already cloned the repository, do so with:

```bash
git clone https://github.com/yourusername/Multi-Agent-Medical-Assistant.git
cd Multi-Agent-Medical-Assistant
```

## Step 2: Create and Activate a Virtual Environment

Create a Python virtual environment to isolate the project dependencies:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

Your command prompt should now show `(venv)` at the beginning, indicating that the virtual environment is active.

## Step 3: Install Dependencies

Install all required packages using pip:

```bash
pip install -r requirements.txt
```

This may take a few minutes as it installs all the necessary libraries.

## Step 4: Configure Environment Variables

1. Copy the example environment file to create your own:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your API keys and configuration:

```bash
# For OpenRouter (recommended):
OPENAI_API_BASE=https://openrouter.ai/api/v1
openai_api_key=your_api_key_here
model_name=openai/gpt-4o-mini  # or another model of your choice

# For embedding model:
embedding_model_name=text-embedding-ada-002

# Optional: If you're using ElevenLabs for text-to-speech
ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here
```

## Step 5: Prepare the RAG System (Optional)

If you want to use the RAG (Retrieval-Augmented Generation) capabilities, you'll need to ingest your documents:

```bash
python ingest_rag_data.py
```

This will process documents in the `./data/documents` directory and create vector embeddings for them.

## Step 6: Run the Application

You need to run both the FastAPI backend and the Flask frontend in separate terminal windows.

### Terminal 1: Start the FastAPI Backend

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Start the FastAPI backend
uvicorn api.fastapi_backend:app --reload --port 8001
```

### Terminal 2: Start the Flask Frontend

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Start the Flask frontend
python app.py
```

The Flask app will run on http://127.0.0.1:5000 by default.

## Step 7: Access the Application

Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

You should now see the Multi-Agent Medical Assistant interface.

## Troubleshooting

### Connection Refused Error

If you see a "Connection refused" error when using the frontend, make sure the FastAPI backend is running on port 8001.

### Missing Modules

If you encounter "ModuleNotFoundError", ensure you've:
1. Activated the virtual environment
2. Installed all requirements with `pip install -r requirements.txt`
3. Are using the correct Python version (3.11+)

### API Key Issues

If you're getting authentication errors:
1. Check that your API keys in the `.env` file are correct
2. Ensure the model you're trying to use is available with your API key

## Docker Setup (Alternative)

The project also includes Docker support for containerized deployment:

```bash
# Build and start the containers
docker-compose up -d

# To stop the containers
docker-compose down
```

## Additional Notes

- The application uses OpenRouter by default, which provides access to various LLM models
- Make sure both the backend and frontend are running simultaneously
- Always run commands from within the activated virtual environment
- If you change the model in the `.env` file, you'll need to restart both the backend and frontend
