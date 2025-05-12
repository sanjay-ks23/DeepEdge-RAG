# LLM-Based RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system powered by a Large Language Model. The system allows users to ask questions through a chat interface, retrieves relevant information from the internet, and generates informative answers based on the latest web content. It features conversation memory to maintain context across interactions.

## Features

- **Web Search Integration**: Searches the internet for relevant content using Serper API
- **Content Extraction**: Scrapes useful text from web pages
- **Intelligent Answer Generation**: Uses OpenAI's models to generate accurate responses
- **Chat Memory**: Maintains conversation context for more natural interactions
- **User-Friendly Interface**: Clean, intuitive Streamlit-based chat interface

## System Architecture

1. **Streamlit Frontend**: Provides the user interface for queries and displays answers
2. **Flask Backend**: Handles API requests, search, content processing, and LLM integration
3. **Search & Retrieval**: Fetches relevant web content using Serper API
4. **Content Processing**: Extracts and formats webpage content for the LLM
5. **LLM Integration**: Generates informative answers using OpenAI's API

## Prerequisites

- Python 3.8 or higher
- Serper API key (for web search)
- OpenAI API key (for LLM capabilities)

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/llm-rag-system.git
cd llm-rag-system
```

### Step 2: Create a Virtual Environment

```bash
# For Windows
python -m venv env
env\Scripts\activate

# For macOS/Linux
python -m venv env
source env/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Keys

Create a `.env` file in the root directory with the following content:

```
SERPER_API_KEY=your_serper_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Replace the placeholder values with your actual API keys.

## Running the Application

### Method 1: Using Provided Scripts

#### For Windows:

Simply double-click the `run.bat` file, or run it from the command prompt:

```bash
run.bat
```

#### For macOS/Linux:

Make the script executable and run it:

```bash
chmod +x run.sh
./run.sh
```

These scripts will:
- Activate the virtual environment
- Install dependencies if needed
- Start both the Flask backend and Streamlit frontend
- Open the necessary terminal windows

### Method 2: Manual Startup

#### Step 1: Start the Flask Backend

Open a terminal window, navigate to the project directory, and run:

```bash
# Activate virtual environment if not already activated
# Windows: env\Scripts\activate
# macOS/Linux: source env/bin/activate

cd flask_app
python app.py
```

You should see: `Running on http://localhost:5001`

#### Step 2: Start the Streamlit Frontend

Open another terminal window, navigate to the project directory, and run:

```bash
# Activate virtual environment if needed
cd streamlit_app
streamlit run app.py
```

#### Step 3: Access the Application

Open your web browser and go to:
```
http://localhost:8501
```

## Using the RAG System

1. Type your question in the input field at the bottom of the page
2. Press Enter or click the Send button
3. Wait for the system to search, retrieve content, and generate an answer
4. View the response in the chat interface
5. Continue the conversation with follow-up questions

To clear the conversation history, click the "Reset Conversation" button in the sidebar.

## Troubleshooting

### Common Issues:

1. **API Key Errors**:
   - Check that your API keys are correctly set in the `.env` file
   - Verify API key permissions and usage limits

2. **Connection Errors**:
   - Ensure both Flask and Streamlit servers are running
   - Check for firewall or network issues

3. **Package Import Errors**:
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+ required)

4. **OpenAI Version Issues**:
   If you see errors related to OpenAI API format, try one of these solutions:
   - Install a specific OpenAI version: `pip install openai==0.28`
   - OR run the OpenAI migration tool: `openai migrate`

5. **Port Conflicts**:
   - If ports 5001 or 8501 are already in use, modify the port numbers in the code

### Getting Help:

If you encounter issues not covered here, please:
1. Check the terminal outputs for specific error messages
2. Review the OpenAI and Serper API documentation for API-specific issues

## Project Structure

```
.
├── .env                  # Environment variables (API keys)
├── requirements.txt      # Project dependencies
├── run.bat               # Windows startup script
├── run.sh                # macOS/Linux startup script
├── README.md             # This documentation
├── flask_app/
│   ├── __init__.py       # Package initialization
│   ├── app.py            # Flask application and API routes
│   └── utils.py          # Utility functions (search, scraping, LLM)
└── streamlit_app/
    └── app.py            # Streamlit frontend application
```

## Extending the Project

Consider these enhancements to the RAG system:

- Add document source citations
- Implement result caching for faster responses
- Add user authentication and session management
- Expand to include PDF and document upload capabilities
- Integrate vector database for more efficient retrieval

## License

[MIT License](LICENSE)

## Acknowledgements

- This project uses OpenAI's API for text generation
- Serper API for web search capabilities
- Streamlit and Flask for the user interface and backend
- BeautifulSoup for web scraping
